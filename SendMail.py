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

### SendMail.py - To send a mail message using SMTP

# $Workfile: SendMail.py $
# $Revision: 8 $
# $Modtime: 16/12/09 9:13 $
# $Author: Jonathan $ 

# Import system stuff
import datetime
import os
import smtplib
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

# Import our stuff
from Config import GetValue


#####
# To send a mail message
###
def mail( serverURL, sender, to, subject, text, Out ):
  """
  Usage:
  mail('somemailserver.com', 'me@example.com', 'someone@example.com', 'test', 'This is a test')
  """
  
  if serverURL == None or serverURL == '':
    Out.OutputInfo( 'No Server to use to send the message' )
  else:
    try:
      # Header
      headers = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % ( sender, to, subject )
      
      # Message - which has the header and the body of the test
      message = headers + text
      
      # Perform the actual sending
      mailServer = smtplib.SMTP( serverURL )
      mailServer.sendmail( sender, to, message )
      mailServer.quit( )
    
    except KeyboardInterrupt:
      Out.OutputError( 'Keyboard interrupt detected', False )
      raise
    
    except:
      Out.OutputError( 'Attempting to send SMTP message', True )
      Out.OutputException( sys.exc_info( ), True )
  
  return
#####


#####
# To send a mail message
# 
# Original from Jordon Mears
# http://www.finefrog.com/2008/05/06/sending-email-with-attachments-in-python/
###
def send_mail( send_to, message_subject, message_text, Out, message_html = "", send_from = "", files = [], send_cc = [], send_bcc = [], mail_server = "localhost" ):
  try:
    # Assertions
    assert type( send_to ) == list
    assert type( files ) == list
    assert type( send_cc ) == list
    assert type( send_bcc ) == list
    
    # Build the message
    message = MIMEMultipart( 'related' )
    message[ 'From' ] = send_from
    message[ 'To' ] = COMMASPACE.join( send_to )
    message[ 'Date' ] = formatdate( localtime = True )
    message[ 'Subject' ] = message_subject
    message[ 'Cc' ] = COMMASPACE.join( send_cc )
    message.attach( MIMEText( message_text ) )
    
    # Attachments
    for f in files:
      part = MIMEBase( 'application', 'octet-stream' )
      part.set_payload( open( f, 'rb' ).read( ) )
      Encoders.encode_base64( part )
      part.add_header( 'Content-Disposition', 'attachment; filename="%s"' % os.path.basename( f ) )
      message.attach( part )
    
    # Now who it's going to
    addresses = []
    for adr in send_to:
      addresses.append( adr )
    for adr in send_cc:
      addresses.append( adr )
    for adr in send_bcc:
      addresses.append( adr )
    
    # Now send it
    if ( len( addresses ) > 0 ):
      smtp = smtplib.SMTP( mail_server )
      smtp.sendmail( send_from, addresses, message.as_string( ) )
      smtp.close( )
    else:
      Out.OutputError( 'No addressees to send the e-mail to', True )
  
  except KeyboardInterrupt:
    Out.OutputError( 'Keyboard interrupt detected', False )
    raise
  
  except:
    Out.OutputError( 'Attempting to send SMTP message', True )
    Out.OutputException( sys.exc_info( ), True )
  
  return
#####


#####
# To send a mail message
###
def SendMailMessageSimple1( sFilename, sAdditional, Out ):
  # Use the main function
  SendMailMessageFull( sFilename, '', '', sAdditional, '', Out )
  return
#####


#####
# To send a mail message
###
def SendMailMessageSimple2( sFilename, sBody, sAdditional, Out ):
  # Use the main function
  SendMailMessageFull( sFilename, '', sBody, sAdditional, '', Out )
  return
#####


#####
# To send a mail message
###
def SendMailMessageFull( sFilename, sSubject, sBody, sAdditional, sCC, Out, bIncludeError = True ):
  """To send a message with a specific subject overide"""
  # Get the various values that we need
  sServer = GetValue( sFilename, 'SMTPServer', Out )
  
  if ( sServer <> '' ):
    sMyName = GetValue( sFilename, 'MyName',      Out )
    sTo     = GetValue( sFilename, 'SMTPTo',      Out )
    sFrom   = GetValue( sFilename, 'SMTPFrom',    Out )
    
    # Do we override the body
    if ( sBody == '' ):
      sBody = GetValue( sFilename, 'SMTPBody', Out )
    
    # Do we override the subject
    if ( sSubject == '' ):
      sSubject = GetValue( sFilename, 'SMTPSubject', Out )
    
    # Info messages
    Out.OutputInfo( 'Sending e-mail to: ' + sTo + '...' )
    if ( len( sCC ) > 0 ):
      Out.OutputInfo( '... cc: ' + sCC + '...' )
    Out.OutputInfo( '... regarding ' + sSubject + '...' )
    Out.OutputInfo( '... ' + sAdditional )
          
    # Any Error Message
    sErrorMsg = ''
    if ( bIncludeError == True ):
      sErrorMsg = Out.GetErrorMessage( )
    
    # Build the body of the message
    dtNow = datetime.datetime.now( )
    sMessageBody = dtNow.strftime( "%a, %d %b %Y %H:%M" ) + '\n\n'
    if ( sMyName <> '' ):
      sMessageBody += 'Name: ' + sMyName + '\n\n'
    if ( sBody <> '' and sBody <> ' ' ):
      sMessageBody += sBody + '\n\n'
    if ( sAdditional <> '' ):
      sMessageBody += sAdditional + '\n\n'
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
    send_mail( send_to = lTo, send_cc = lCC, message_subject = sSubject, message_text = sMessageBody, send_from = sFrom, mail_server = sServer, Out = Out )
  else:
    # Indicate we couldn't send
    Out.OutputInfo( 'No configuration for SendMail' )
    
    return
#####
