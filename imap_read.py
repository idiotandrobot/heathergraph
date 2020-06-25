import imaplib
import email
import email.header
import datetime
import re
import html_parse
import logging
log = logging.getLogger(__name__)

def navigate_content(content, level=0):
    ctype = content.get_content_type()
    cdispo = str(content.get('Content-Disposition'))
    log.info('{0} + {1} {2}'.format(' ' * level, ctype, cdispo))
    if content.is_multipart():
        for payload in content.get_payload():
            navigate_content(payload, level + 1)   

def read_content(content):    
    try:
        text = '++ No Content ++'
        if content.is_multipart():
            for part in content.walk():
                has_text, rtext = read_text(part)
                if has_text:
                    text = rtext
                    break
        else:
            has_text, rtext = read_text(content)
            if has_text:
                text = rtext
        return text
    except:
        log.exception('read_content')
        return '++ No Potatoes Error ++'

def read_text(content):
    has_text = False
    text = ''
    ptype = content.get_content_type().split("/")    
    if ptype[0] == 'text':
        bytes = content.get_payload(decode=True)
        charset = content.get_content_charset('iso-8859-1')
        text = bytes.decode(charset, 'replace')
        has_text = True
        if ptype[1] == 'html':
            has_text = False
            text = html_parse.parse(text)
            has_text = True
    return has_text, text

def read_subject(message):
    try:
        subject = email.header.decode_header(message['Subject'])[0]
        if subject[1] == None:
            actual_subject = unicode(subject[0])
        else:
            actual_subject = subject[0].decode(subject[1])
        return actual_subject
    except:
        log.exception('read_subject')
        return '++ Subject Error ++'

def read_date(message):
    try:
        date_tuple = email.utils.parsedate_tz(message['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            return local_date.strftime('%a, %d %b %Y %H:%M:%S')
    except:
        return '++ Date Error ++'

def read_from(message):
    try:
        return str(email.header.make_header(email.header.decode_header(message['From'])))
    except:
        return ''

def read_message(mailbox, num, message_handler = None):
    response, data = mailbox.fetch(num, '(RFC822)')
    if response != 'OK':
        log.warning('Could not fetch message %s', num)
        return

    message = email.message_from_string(data[0][1])
    log.info('Message %s', num)
    log.info('Date: %s', message['Date'])
    log.info('Content:')
    navigate_content(message, 0)

    if message_handler != None:
        message_handler(
        read_from(message), 
        read_date(message), 
        read_subject(message),
        read_content(message))
       

def read_folder(mailbox, folder_name, message_handler = None):
    response, data = mailbox.select(folder_name)
    if response == 'OK':
        log.info('Processing %s folder...', folder_name)
        read_current_folder(mailbox, message_handler)
        mailbox.close()
        log.info('Processing complete')
    else:
        log.warning('Unable to open %s folder', folder_name)

def read_current_folder(mailbox, message_handler = None):

    response, data = mailbox.search(None, 'UNSEEN')
    if response != 'OK':
        log.warning('No messages found!')
        return

    for num in data[0].split():
        try:
            read_message(mailbox, num, message_handler)
        except:
            log.exception('Unable to read message %s', num)

