import imaplib
import time
import imap_read

def is_bye(response):
    return response.startswith('* BYE ') or (len(response) == 0)

def is_new_mail(response):
    splitline = response.split()
    return len(splitline) == 3 and splitline[2] == 'EXISTS'

def is_flagged_unread(response):
    splitline = response.split()
    return len(splitline) == 7 and splitline[2] == 'FETCH' and splitline[6] == '())'

def message_id(response):
    try:
        return response.split()[1]
    except:
        return None

def send_idle(mailbox):
    mailbox.send('%s IDLE\r\n'%(mailbox._new_tag()))

def send_done(mailbox):
    mailbox.send(b'DONE\r\n')

def monitor_folder(mailbox, foldername, mail_handler = None):
    try:
        mailbox.select(foldername, readonly=True)
        send_idle(mailbox)
        print '++ Waiting...'      
        while True:        
            line = mailbox.readline().strip()
            print '++>', line
            if is_bye(line):
                print '++ Time to go'
                break
            splitline = line.split()
            if is_new_mail(line):
                print "++ You've got mail"
                if mail_handler != None: mail_handler()                
            if is_flagged_unread(line):
                print "++ Mail flagged unread"
                if mail_handler != None: mail_handler()              
    finally:
        try:
            print '++ Closing...'
            c.close()
        except:
            pass