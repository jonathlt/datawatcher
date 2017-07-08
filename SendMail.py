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
# 
# Original from Jordon Mears
# http://www.finefrog.com/2008/05/06/sending-email-with-attachments-in-python/
###
def send_mail( send_to, message_subject, message_text, Out, message_html = "", send_from = "", files = [], send_cc = [], send_bcc = [], mail_server = "localhost", smtp_user = "", smtp_password = "" ):
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
      Out.OutputInfo('Sending from send_mail function')
      #smtp = smtplib.SMTP( mail_server )
      #smtp.sendmail( send_from, addresses, message.as_string( ) )
      #smtp.close( )
      mailServer = smtplib.SMTP_SSL( mail_server , 465)
      mailServer.ehlo()
      mailServer.login(smtp_user, smtp_password)	  
      mailServer.sendmail( send_from, send_to, message.as_string() )
      mailServer.close( )
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
