## Copyright (c) 2009 Astun Technology

## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
## copies of the Software, and to permit persons to whom the Software is
## furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
## OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
## THE SOFTWARE.

###
import pyodbc
import os
import sys
import pg
from xml.sax.saxutils import escape

# Import Astun stuff
import Output
from Config import GetValue

class DataCompare:
  _conn1 = 0
  _sConfigFile = ''
  
  #####
  # To instantiate self
  ###
  def __init__(self, sConfigFile, Out ):
    self._conn = 0
    self._sConfigFile = sConfigFile
    self._output = Out
    self._bError = False
    self._sCreateSQL = ''
  #####

  #####
  # 
  ###
  def FindDifferences(self,sQuery):
    
    ## Connect to the Postgres database
    self._conn = 0
    self.OpenPostgres()
  
    ## Check that TABLENAME and TABLENAME_LASTUPDATE both exist
    sDestTable = GetValue(self._sConfigFile,sQuery + 'DestTable',self._output)
    sUniqueKey = GetValue(self._sConfigFile,sQuery + 'UniqueKey',self._output)
  
    ## Create a view containing the difference data
    sSQL = 'SELECT at_CompareTablesWithKey(\'' + sDestTable + '\'' + ',' + '\'' + sUniqueKey + '\'' + ');'   
    result = self._conn.query(sSQL).getresult( )[0][0]
  
    if (int(result) != 0):
      ## An error has ocurred creating the difference view
      self._output.OutputError('Problem importing data.',True)
      raise
    else:
      
      try:
        ## Write out the results of the compare to an XML file
        sSQL = 'SELECT * FROM "' + sDestTable + '_view2" ' + ' ORDER BY "STATUS","' + sUniqueKey + '";'
        returnlist = self._conn.query(sSQL).dictresult()
    
        sXML = '<table name=\'' + sDestTable + '\'' + '>'
        sXML += '<rows>'
    
        for dict in returnlist:
          sXML += '<row>'
          for key,value in dict.items():
            ## Make sure that any XML characters are converted eg & = &amp; etc
            sValueIn = escape(value)
            sXML += '<' + key + '>' + sValueIn + '</' + key + '>'
          sXML += '</row>'
    
        sXML += '</rows>'
        sXML += '</table>'
    
        file = open('email.xml','w')
        file.write(sXML)      
        file.close()
      except:
        self._output.OutputError('Problem getting results and writing to xml')
        self._output.OutputException( sys.exc_info( ), True )
        raise
      finally:
        self.ClosePostGres()
    return
  
  #####
  ## Import data from source database, perform any table renaming
  ###
  def ImportData(self,sQuery):
  
    bTableExists = False
  
    sSourceConn = GetValue(self._sConfigFile,sQuery + 'SourceConn',self._output)
    sDestTable  = GetValue(self._sConfigFile,sQuery + 'DestTable',self._output)
    sSQL  = GetValue(self._sConfigFile,sQuery + 'SQL',self._output)
  
    ## Get source table data
    self.GetSourceTableData(sSourceConn,sSQL,sDestTable)

    ## Connect to the Postgres database
    self.OpenPostgres()
  
    ## Make sure the Postgres database is closed if there are any errors
  
    try:
      ## Check to see if the old table exists to decide whether to
      ## go any further
      if (self.CheckTableExists(sDestTable) == True):
    
        ## Rename the old table to tableName_LASTUPDATE
        self.RenameTable(sDestTable)
        bTableExists = True
    
      ## Create the new table in the Postgres database
      self._conn.query(self._sCreateSQL)
    
      ## Import data from the external database
      self.DoImport(sDestTable)
  
    except:
      self._output.OutputError('Problem importing data.',True)
      raise
    finally:
      self.ClosePostGres()
    
    return bTableExists
  
  #####
  # Open connection to postgres
  ###
  def OpenPostgres(self):
    result = None
  
    ## To ensure we have a connection
    if ( self._conn == 0):
      self._output.OutputInfo( 'Opening PostgreSQL connection' )
    
    try:
      # Get the config settings
      sHost = GetValue( self._sConfigFile, 'PGHost', self._output )
      sDatabase = GetValue( self._sConfigFile, 'PGDBName', self._output )
      sUser     = GetValue( self._sConfigFile, 'PGUser', self._output )
      sPwd      = GetValue( self._sConfigFile, 'PGPwd', self._output )
    
      # Now connect
      self._conn = pg.connect( host=sHost, user=sUser, dbname=sDatabase, passwd=sPwd )
    
    except KeyboardInterrupt:
      Out.OutputError('Keyboard interrupt detected', False )
      raise
    
    except:
      self._output.OutputError( 'On connecting to Postgres DB',True)
      self._output.OutputException( sys.exc_info( ), True)
      self._bError = True
  
    return
  #####

  #####
  # Close a connection
  ###
  def ClosePostGres( self ):
  # Close the connection
    if self._conn <> 0:
      self._output.OutputInfo( 'Closing PostgreSQL connection...' )
    
    try:
      self._conn.close( )
    
    except KeyboardInterrupt:
      Out.OutputError( 'Keyboard interrupt detected', False )
      raise
    
    except:
      self._output.OutputError( 'On closing PostgresSQL connection', True )
      self._output,OutputException( sys.exc_info( ), True )
      self._conn = 0
    
    return
  #####

  #####
  # Query the source database for the table information
  # Build SQL to create the new table in Postgres
  # Create a text file containing data to copy
  ###
  def GetSourceTableData(self,sSourceConn,sSQL,sDestTable):
  
    self._output.OutputInfo( 'Getting source table data' )
  
    connsrc = pyodbc.connect(sSourceConn)
    cursor = connsrc.cursor()
  
    try:

      ## JLT 24.09.2009 moved to try block in case of failure
      file = open("dump.txt",'w')
   
      cursor.execute(sSQL)

      ## Iterate through the cursor results and build a file to perform a copy command on
      rows = cursor.fetchall()
   
      self._sCreateSQL = 'CREATE TABLE ' + '"' + sDestTable + '" ( '
     
      for column in cursor.description: 
        self._sCreateSQL += '"' + column[0] + '" TEXT' + ","
     
      self._sCreateSQL = self._sCreateSQL[:-1]
      self._sCreateSQL += " ) "
    
      for row in rows:
        colNo = 0
        sRowText = ""
        for column in cursor.description:
          ## Replace any \n or \r with empty string as this interferes with the import
          sTextIn = str(row[colNo])
          sTextIn = sTextIn.replace("\n","")
          sTextIn = sTextIn.replace("\r","")
          ## JLT 24.09.2009 replace special characters before importing to postgres
          sTextIn = sTextIn.replace("\\","\\\\")
          sTextIn = sTextIn.replace("~","\\~")
          sTextIn = self.RemoveNonAscii(sTextIn)
          ## End
          sRowText += sTextIn + '~'
          colNo+=1
        sRowText = sRowText[:-1]
        file.write(sRowText)
        file.write('\n')
  
  
    except KeyboardInterrupt:
      self._output.OutputError( 'Keyboard interrupt detected', False)
      raise
    except:
      self._output.OutputError('On building SQL/Writing dump file')
      self._output.OutputException( sys.exc_info(),True)
      raise
    finally:
      file.close()  
      cursor.close()
      connsrc.close()
  
    return
  
  #####
  # Check that the table exists
  ###
  def CheckTableExists(self,sTableName):
  
    self._output.OutputInfo( 'Checking table exists' )
  
    bTableExists = False
    sTableExistsSQL = 'SELECT at_sys_exists_table(\'' + sTableName + '\')'
    result = self._conn.query( sTableExistsSQL ).getresult( )[0][0]
    if (result <> 0):
      bTableExists = True
    return bTableExists
  
  #####
  # Rename the existing table to x_LASTUPDATE
  # Drop the current table
  ###
  def RenameTable(self, sTableName):
  
    self._output.OutputInfo( 'Renaming table' )
  
    try:
      if (self.CheckTableExists(sTableName + '_LASTUPDATE') == True):
        sDropSQL = 'DROP TABLE "' + sTableName + '_LASTUPDATE' + '" CASCADE'
        self._conn.query(sDropSQL)
      sRenameSQL = 'ALTER TABLE "' + sTableName + '" RENAME TO "' + sTableName + '_LASTUPDATE"'
      self._conn.query(sRenameSQL)
    except KeyboardInterrupt:
      self._output.OutputError( 'Keyboard interrupt detected', False)
      raise
    except:
      self._output.OutputError('On dropping/renaming Postgres table', True)
      self._output.OutputException( sys.exc_info( ), True)
      raise
    
    return
  
  #####
  # Copy the data from the dump file to the database
  ###
  def DoImport(self, sTableName):
  
    self._output.OutputInfo( 'Copying from the dump file to the database.' )
  
    ## Import data in the dump.txt file to the Postgres database
    sCopySQL = 'COPY "' + sTableName + '" FROM ' + 'E' + '\'' + sys.path[0] + '\\' + 'dump.txt\'' + ' WITH DELIMITER \'~\''
    sCopySQL = sCopySQL.replace('\\','\\\\')
    try:
      self._conn.query(sCopySQL)
    except KeyboardInterrupt:
      self._output.OutputError( 'Keyboard interrupt detected', False )
      raise
    except:
      self._output.OutputError( 'On copying data from file to Postgres table', True )
      self._output.OutputException( sys.exc_info( ), True )
      raise
    return

  #####
  # Helper function to remove non-ascii chars
  ###
  def RemoveNonAscii(self, sInput):

    sTemp = ""
    for x in sInput:
      if ord(x) < 128:
        sTemp+= x
      else:
        sTemp+= '?'

    return sTemp
    
    

       


