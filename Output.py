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

### Output.py - Class to output various information to output stream, and to log to file

# $Workfile: Output.py $
# $Revision: 8 $
# $Modtime: 16/12/09 9:10 $
# $Author: Jonathan $ 

# Import system stuff
import datetime
import os.path
import sys
from string import split
from traceback import format_tb

# Import our stuff


# Constants
OUTPUTLEVEL_ALWAYS    = 7
OUTPUTLEVEL_NONE      = 6
OUTPUTLEVEL_EXCEPTION = 5
OUTPUTLEVEL_ERROR     = 4
OUTPUTLEVEL_WARNING   = 3
OUTPUTLEVEL_INFO      = 2
OUTPUTLEVEL_DEBUG     = 1
OUTPUTLEVEL_ALL       = 0


class ClassOutput:
  #####
  # To initialiate self
  ###
  def __init__( self, sName ):
    self._outputlevel = OUTPUTLEVEL_WARNING
    self._file        = "Output.log"
    self._tofile      = False
    self._sMsg        = ''
    self._lMax        = 20000
    
    # Set the name
    self._sName = sName[ 0:6 ]
    iLen = len( self._sName )
    if ( iLen < 6 ):
      for iIndex in range( iLen, 6 ):
        self._sName += ' '
  #####
  
  
  #####
  # Output for debugging, etc
  ###
  def Output( self, iLevel, sMsg, bToFile, bToScreen ):
    # Only output level asked for
    if ( iLevel >= self._outputlevel ):
      if ( iLevel == OUTPUTLEVEL_ALWAYS ):
        if ( bToScreen == True ):
          print self._sName, sMsg
        if ( bToFile == True ):
          self.LogMessage( '', sMsg )
      elif ( iLevel == OUTPUTLEVEL_EXCEPTION ):
        if ( bToScreen == True ):
          print self._sName, 'EXCEPTION:', sMsg
        if ( bToFile == True ):
          self.LogException( sMsg )
      elif ( iLevel == OUTPUTLEVEL_ERROR ):
        if ( bToScreen == True ):
          print self._sName, 'ERROR:', sMsg
        if ( bToFile == True ):
          self.LogMessage( 'ERROR:', sMsg )
      elif ( iLevel == OUTPUTLEVEL_WARNING ):
        if ( bToScreen == True ):
          print self._sName, 'WARNING:', sMsg
        if ( bToFile == True ):
          self.LogMessage( 'WARNING:', sMsg )
      elif ( iLevel == OUTPUTLEVEL_INFO ):
        if ( bToScreen == True ):
          print self._sName, 'INFO:', sMsg
        if ( bToFile == True ):
          self.LogMessage( 'INFO:', sMsg )
      elif ( iLevel == OUTPUTLEVEL_DEBUG ):
        if ( bToScreen == True ):
          print self._sName, 'DEBUG:', sMsg
        if ( bToFile == True ):
          self.LogMessage( 'DEBUG:', sMsg )
    
    return
  #####
  
  
  #####
  # Log the message
  ###
  def LogMessage( self, sType, sMsg ):
    if ( self._tofile == True ):
      try:
        now = datetime.datetime.now( )
        # Open
        f = open( 'Logs\\' + self._file, 'a' )
        f.write( now.strftime( "%a, %d %b %Y %H:%M:%S " ) )
        f.write( self._sName + ": " )
        f.write( sType )
        f.write( sMsg )
        f.write( '\n' )
        f.close( )
      
        # Now check if the files need to be rolled over
        self.CheckFileSizeX( )

      except KeyboardInterrupt:
        print 'Keyboard interrupt detected'
        raise
      
      except:
        print 'ERROR: Writing to logger'
        print 'EXCEPTION:', sys.exc_info( )
    
    return
  #####
  
  
  #####
  # Log the message
  ###
  def LogException( self, exc ):
    if ( self._tofile == True ):
      try:
        # Get the individual tuple bits of the exception
        ex1, ex2, ex3 = exc
        now = datetime.datetime.now( )
        # Open
        f = open( 'Logs\\' + self._file, 'a' )
        f.write( now.strftime( "%a, %d %b %Y %H:%M:%S " ) )
        f.write( 'EXCEPTION:' )
        f.write( str( ex1 ) )
        f.write( '\n' )
        f.write( str( ex2 ) )
        f.write( '\n' )
        f.write( 'TRACEBACK:' )
        for sItem in format_tb( ex3 ):
          f.write( sItem )
        f.close( )
        
        # Hold the exception message
        self._sMsg = str( ex1 ) + ' ' + str( ex2 )
        
        # Now check if the files need to be rolled over
        self.CheckFileSizeX( )
      
      except KeyboardInterrupt:
        print 'Keyboard interrupt detected'
        raise
      
      except:
        print 'ERROR: Writing to logger'
        print 'EXCEPTION:', sys.exc_info( )
    
    return
  #####
  
  
  #####
  # Output Debug
  ###
  def OutputDebug( self, sMsg, bToFile = True, bToScreen = True ):
    self.Output( OUTPUTLEVEL_DEBUG, sMsg, bToFile, bToScreen )
  #####
  
  
  #####
  # Output Info
  ###
  def OutputInfo( self, sMsg, bToFile = True, bToScreen = True ):
    self.Output( OUTPUTLEVEL_INFO, sMsg, bToFile, bToScreen )
  #####
  
  
  #####
  # Output Warning
  ###
  def OutputWarning( self, sMsg, bToFile = True, bToScreen = True ):
    self.Output( OUTPUTLEVEL_WARNING, sMsg, bToFile, bToScreen )
  #####
  
  
  #####
  # Output Error
  ###
  def OutputError( self, sMsg, bToFile = True, bToScreen = True ):
    self._sMsg = sMsg
    self.Output( OUTPUTLEVEL_ERROR, sMsg, bToFile, bToScreen )
  #####
  
  
  #####
  # Output Exception
  ###
  def OutputException( self, ex, bToFile = True, bToScreen = True ):
    self.Output( OUTPUTLEVEL_EXCEPTION, ex, bToFile, bToScreen )
  #####
  
  
  #####
  # Output Always
  ###
  def OutputAlways( self, sMsg, bToFile = True, bToScreen = True ):
    self.Output( OUTPUTLEVEL_ALWAYS, sMsg, bToFile, bToScreen )
  #####
  
  
  #####
  # Set Output level
  ###
  def SetOutputLevel( self, iLevel ):
    # Set the output level
    self._outputlevel = iLevel
  #####
  
  
  #####
  # Check the file size and roll files
  ###
  def CheckFileSizeX( self ):
    # Only if the thing exists
    if ( os.path.exists( "Logs\\" + self._file ) ):
      # Get the filesize
      fsize = os.path.getsize( "Logs\\" + self._file )
      if ( fsize > self._lMax ):
        # Roll the files
        self.RollFiles( self._file )
  #####
  
  
  #####
  # To Change the max file size
  ###
  def SetFileMax( self, lMax ):
    """To set the maximum file size for logs files"""
    self._lMax = lMax
  #####
  
  
  #####
  # Change the output file for logging
  ###
  def SetFilename( self, sFilename ):
    """Set the Output filename"""
    self._file = sFilename
    #if self._tofile == True:
    #  # Check the File sizes
    #  self.CheckFileSizeX( )
  #####
  
  
  #####
  # Set Logging to file
  ###
  def SetFileLogging( self, bValue ):
    self._tofile = bValue
    if ( bValue == True ):
      if ( os.path.exists( "Logs" ) == False ):
        os.mkdir( "Logs" )
      #else:
      #  # check the file size
      #  self.CheckFileSizeX( )
  #####
  
  
  #####
  # Check and copy 
  ###
  def CheckAndCopy( self, sFile1, sFile2 ):
    if ( os.path.exists( sFile1 ) ):
      os.rename( sFile1, sFile2 )
  #####
  
  
  #####
  # Rolling files
  ###
  def RollFiles( self, sFilename ):
    sBits = split( sFilename, "." )
    sStub = "Logs\\" + sBits[0]
    
    # Remove the last one
    sFile1 = sStub + "_9.log"
    if ( os.path.exists( sFile1 ) ):
      os.remove( sFile1 )
    
    # Work backwards
    sFile2 = sFile1
    sFile1 = sStub + "_8.log"
    self.CheckAndCopy( sFile1, sFile2 )
    sFile2 = sFile1
    sFile1 = sStub + "_7.log"
    self.CheckAndCopy( sFile1, sFile2 )
    sFile2 = sFile1
    sFile1 = sStub + "_6.log"
    self.CheckAndCopy( sFile1, sFile2 )
    sFile2 = sFile1
    sFile1 = sStub + "_5.log"
    self.CheckAndCopy( sFile1, sFile2 )
    sFile2 = sFile1
    sFile1 = sStub + "_4.log"
    self.CheckAndCopy( sFile1, sFile2 )
    sFile2 = sFile1
    sFile1 = sStub + "_3.log"
    self.CheckAndCopy( sFile1, sFile2 )
    sFile2 = sFile1
    sFile1 = sStub + "_2.log"
    self.CheckAndCopy( sFile1, sFile2 )
    sFile2 = sFile1
    sFile1 = sStub + "_1.log"
    self.CheckAndCopy( sFile1, sFile2 )
    sFile2 = sFile1
    sFile1 = sStub + ".log"
    self.CheckAndCopy( sFile1, sFile2 )
  #####
  
  
  #####
  # To allow the error we are hold to be got at
  ###
  def GetErrorMessage( self ):
    return self._sMsg
  #####
