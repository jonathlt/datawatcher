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

### Config.py - To get a config entry value from a configuration file

# Imprt system stuff
import csv
import os.path
import sys

# Import our stuff


#####
# Get a list of the files to work with
###
def GetConfig( sFilename, Out ):
  try:
    csv.register_dialect( 'Control', delimiter = '=', escapechar = '^', quoting = csv.QUOTE_NONE )
    return csv.reader( open( sFilename, "rb" ), 'Control' )
  
  except KeyboardInterrupt:
    Out.OutputError( 'Keyboard interrupt detected', False )
    raise
  
  except:
    if ( Out <> None ):
      Out.OutputError( 'Unexpected error in control file <' + sFilename + '>', True )
      Out.OutputException( sys.exc_info( ), True )
    return None
#####


#####
# Get the Value of a configuration setting - the first found
###
def GetValue( sFilename, sValue, Out, sDefault = '' ):
  # Return value
  sReturn = sDefault
  
  # All configs in the Config directory
  sFullFilename = 'Config\\' + sFilename
  
  # Check the config file exists
  if ( os.path.exists( sFullFilename ) == True ):
    # Get the configuration settings
    thelist = GetConfig( sFullFilename, Out )
    for entry in thelist:
      if ( len( entry ) > 0 ):
        if ( entry[ 0 ] == sValue ):
          sReturn = entry[ 1 ]
          break
  
  # Return
  return sReturn
#####


#####
# Get the Values of a configuration setting, a list of the lot
###
def GetValues( sFilename, sValue, Out ):
  # Return value
  list = []
  
  # All configs in the Config directory
  sFullFilename = 'Config\\' + sFilename
  
  # Check the config file exists
  if ( os.path.exists( sFullFilename ) == True ):
    # Get the configuration settings
    thelist = GetConfig( sFullFilename, Out )
    for entry in thelist:
      if ( len( entry ) > 0 ):
        if ( entry[ 0 ] == sValue ):
          list.append( entry[ 1 ] )
  
  # Return
  return list
#####


#####
# To check that the config file exists
###
def FileExists( sFilename ):
  bExists = False
  
  # All configs in the Config directory
  sFullFilename = 'Config\\' + sFilename
  
  # Check the config file exists
  if ( os.path.exists( sFullFilename ) == True ):
    bExists = True
  
  return bExists
#####
