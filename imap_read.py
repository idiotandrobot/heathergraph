import imaplib
import email
import email.header
import datetime

def navigate_content(content, level=0):
    ctype = content.get_content_type()
    cdispo = str(content.get('Content-Disposition'))
    print '++',' ' * level, '+', ctype, cdispo
    if content.is_multipart():
        for payload in content.get_payload():
            navigate_content(payload, level + 1)   

def read_content(content):
    if content.is_multipart():
        text = ''
        for payload in content.get_payload():
            text += read_content(payload)
        return text
    elif content.get_content_type() == 'text/plain':
        return unicode(content.get_payload(decode=True), 'utf-8')

    return ''

def read_subject(message):
    try:
        decode = email.header.decode_header(message['Subject'])[0]
        return unicode(decode[0])
    except:
        return '++ No Subject ++'

def read_date(message):
    try:
        date_tuple = email.utils.parsedate_tz(message['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            return local_date.strftime('%a, %d %b %Y %H:%M:%S')
    except:
        return '++ No Date ++'

def read_from(message):
    try:
        return str(email.header.make_header(email.header.decode_header(message['From'])))
    except:
        return ''

def read_message(mailbox, num, message_handler = None):
    response, data = mailbox.fetch(num, '(RFC822)')
    if response != 'OK':
        print '++ Error: Could not fetch message', num
        return

    message = email.message_from_string(data[0][1])
    print '++', "-" * 80
    print '++ Message %s' % num
    print '++ Date:', message['Date']
    print '++ Content:'
    navigate_content(message, 0)
    print '++', "-" * 80

    if message_handler != None:
        message_handler(\
        read_from(message), \
        read_date(message), \
        read_subject(message), \
        read_content(message))
       

def read_folder(mailbox, folder_name, message_handler = None):
    response, data = mailbox.select(folder_name)
    if response == 'OK':
        print '++ Processing', folder_name, 'folder...'
        read_current_folder(mailbox, message_handler)
        mailbox.close()
        print '++ Processing complete'
    else:
        print '++ Error: Unable to open', folder_name, 'folder', response

def read_current_folder(mailbox, message_handler = None):

    response, data = mailbox.search(None, 'UNSEEN')
    if response != 'OK':
        print '++ No messages found!'
        return

    for num in data[0].split():
        try:
            read_message(mailbox, num, message_handler)
        except:
            print '++ Error: Unable to read message', num

