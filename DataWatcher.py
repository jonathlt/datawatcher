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

### DataWatcher.py - Main Process for the DataWatcher process

# Import Astun Stuff
#from SendMail  import SendMailMessageSimple1
from SendMail  import send_mail
import Output
import Config
import Data

# Import Shared
import sys
import datetime

import lxml.etree as ET

class DataWatcher:
 #####
  # To Instantiate this class
  ###
  def __init__( self, params ):
      # Init
      self._bError  = False
      self._dtStart = datetime.datetime.now( )
      self._dtEnd   = datetime.datetime.now( )
      self._bContinue = False
      
      # Get the Output
      self._Out = Output.ClassOutput('DataWatcher')
      
      # Config Filename
      if ( len( params ) < 3 ):
        self._bError = True
      else:
        self._sConfigFile = params[ 1 ]
        
        # Does the config file exist
        if ( Config.FileExists( self._sConfigFile ) == False ):
          self._bConfigError = True
        else:
          self._bConfigError = False
          
        return
  #####
  
  #####
  # XSL Transform 
  ###
  def XSLTransform(self,xmlFile,xslFile):
    
    self._Out.OutputInfo('Transforming xsl')
    
    try:
    
      dom = ET.parse(xmlFile)
      xslt = ET.parse(xslFile)
      transform = ET.XSLT(xslt)
      newdom = transform(dom)
	  
      result = ET.tostring(newdom, pretty_print=True)
    
    except:
      self._Out.OutputError( 'On performing the xsl transform', True )
      self._Out.OutputException( sys.exc_info( ), True )
      raise
    
    return result
  
  #####
  # Send an email to the person specified in SMTPToFail 
  ###
  def SendErrorEmail(self):
    SendMailMessageSimple1(self._sConfigFile,'An error ocurred in the Data comparison process.',self._Out)
    return
  
  #####
  # Send an email to the person specified in SMTPTo with the results attached
  ###
  def SendResultsEmail(self,query):

    sAttachment = self.XSLTransform('email.xml','email.xsl')
    
    file = open('results.html','w')
    file.write(sAttachment)
    file.close()

    sFilename = self._sConfigFile
   
    # Get the various values that we need
    sServer = Config.GetValue( sFilename, 'SMTPServer', self._Out )
      
    if ( sServer <> '' ):
      sMyName = Config.GetValue( sFilename, 'MyName',      self._Out )
      sTo     = Config.GetValue( sFilename, 'SMTPTo',      self._Out )
      sFrom   = Config.GetValue( sFilename, 'SMTPFrom',    self._Out )
      sCC     = Config.GetValue( sFilename, 'SMTPCC',	   self._Out )
     
      sBody   = Config.GetValue( sFilename, 'SMTPBody', self._Out )
      sSubject= Config.GetValue( sFilename, 'SMTPSubject', self._Out )
	  
      sSMTPUser = Config.GetValue( sFilename, 'SMTPUser', self._Out )
      sSMTPPassword = Config.GetValue ( sFilename, 'SMTPPass', self._Out)
        
      # Info messages
      self._Out.OutputInfo( 'Sending e-mail to: ' + sTo + '...' )
      if (sCC <> ''):
        self._Out.OutputInfo( '... cc: ' + sCC + '...' )
      self._Out.OutputInfo( '... regarding ' + sSubject + '...' )
      
      sErrorMsg = self._Out.GetErrorMessage( )
        
      # Build the body of the message
      dtNow = datetime.datetime.now( )

      sMessageBody = dtNow.strftime( "%a, %d %b %Y %H:%M" ) + '\n\n'
      if ( sMyName <> '' ):
        sMessageBody += 'Name: ' + sMyName + '\n\n'
        sMessageBody += 'Query Name: ' + query + '\n\n'
        sMessageBody += 'SQL: ' + Config.GetValue( sFilename, str(query + 'SQL'), self._Out ) + '\n\n'
        sMessageBody += 'Unique Key: ' + Config.GetValue( sFilename, str(query + 'UniqueKey'), self._Out ) + '\n\n'
        sMessageBody += 'Destination Table: ' + Config.GetValue( sFilename, str(query + 'DestTable'), self._Out ) + '\n\n'
        sMessageBody += 'DataWatcher comparison results are attached'
      if ( sBody <> '' and sBody <> ' ' ):
        sMessageBody += sBody + '\n\n'
      if ( sErrorMsg <> '' ):
        sMessageBody += sErrorMsg + '\n\nPlease see the log for more details.'
      
      # Make the lists
      if ( len( sTo ) > 0 and sTo <> '' ):
        lTo = sTo.split( ',' )
      else:
        lTo = []
      if ( len( sCC ) > 0 and sCC <> '' ):
        lCC = sCC.split( ',' )
      else:
        lCC = []
          
      # Do the mail thang
      send_mail( send_to = lTo, send_cc = lCC, message_subject = sSubject, message_text = sMessageBody, send_from = sFrom, mail_server = sServer, Out = self._Out, files = ["results.html"], smtp_user = sSMTPUser, smtp_password = sSMTPPassword)
    else:
      # Indicate we couldn't send
      self._Out.OutputInfo( 'No configuration for SendMail' )
        
    return
    
  
  #####
  # Start the Watcher
  #####
  def DataWatcherStart(self,params):

    if (self._bConfigError == True):
      print 'Cannot find configuration file. Aborting..'
    else:

      # My Name is?
      self._sName = Config.GetValue( self._sConfigFile, 'MyName', self._Out )
          
      # Flesh the Output out
      self._Out.SetFilename( self._sName + '.log' )
      self._Out.SetOutputLevel( Output.OUTPUTLEVEL_INFO )
      self._Out.SetFileLogging( True )

      # Log me
      self._Out.OutputInfo('___________________________')
      self._Out.OutputInfo('DataWatcher starting')

      # Check for Query name, then get SQL,SourceDB and Destination table
      tQueries = Config.GetValues(self._sConfigFile,'Query', self._Out)
      
      for sQuery in tQueries:
        if (sQuery == params[2]):
          self._bContinue = True
          
      sQuery = params[2]
      
      if (self._bContinue == False):
        self._Out.OutputError('Configuration information does not exist for the query ' + params[2])
      else:
        compare = Data.DataCompare(self._sConfigFile, self._Out)
        try:
          bTableExists = compare.ImportData(sQuery)
          # If the table already exists when the import was done, we can do the
          # comparison as we have x and x_LASTUPDATE
          if (bTableExists == True):
            compare.FindDifferences(sQuery)
            self.SendResultsEmail(sQuery)
        except:
          self.SendErrorEmail()
      return 
  
#####
# Main
###
if ( len( sys.argv ) < 3 ):
  print 'Required parameters: <Configuration Filename> <QueryName>'
else:
  control = DataWatcher( sys.argv )
  control.DataWatcherStart( sys.argv )
#####  

