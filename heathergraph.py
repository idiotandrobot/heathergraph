import platform
def linux_check():
    return platform.system() == 'Linux'

import argparse
import signal
import sys
import time
import os

import dir
dir = dir.Dir.root()

import config
config = config.Config(dir.filepath('heathergraph.ini'))

import imaplib
import imap_connect
import imap_read
import imap_idle
from throttle import throttle
if linux_check():
    import pipsta
import logging
import logging.config
log = logging.getLogger(__name__)

#imaplib.Debug = 4

MONITOR_POLL_PERIOD = 3

def parse_arguments():
    parser = argparse.ArgumentParser(description='Monitors IMAP and prints messages')
    return parser.parse_args()

def signal_handler(sig_int, frame):
    del sig_int, frame
    sys.exit()

@throttle(seconds=5)
def process_mail():
    mailbox = imap_connect.open_connection(config)
    try:
        imap_read.read_folder(mailbox, config.folder, print_message)
    finally:
        mailbox.logout()

def print_message(sender, date, subject, content):

    try:
        sender = sender.split()[0]
    except:
        pass

    message = {
        'from': sender,
        'date': date,
        'subject': subject.encode('utf-8', config.encodingerrors),
        'content': content.encode('utf-8', config.encodingerrors)
    }

    with open(dir.subdir('templates').filepath(config.template), 'r') as f:
        template = f.read()
    
    txt = template.format(**message).decode('utf-8')
    log.debug('Message:\r\n' + txt)

    asc = txt.encode('ascii', config.encodingerrors)
    log.info('ASCII:\r\n' + asc)
    
    if linux_check():
        pipsta.print_to_pipsta(asc) 
   
def monitor_mail():
    mailbox = imap_connect.open_connection(config)
    try:
        imap_idle.monitor_folder(mailbox, config.folder, process_mail)
    finally:
        mailbox.logout()    
        
def start_up_print():
    with open(dir.subdir('templates').filepath(config.startuptemplate), 'r') as f:
        txt = f.read()        
    log.info('Greeting:\r\n' + txt)
    if linux_check():
        pipsta.print_to_pipsta(txt)


def main():
    parse_arguments()
        
    signal.signal(signal.SIGINT, signal_handler)    

    # Needed at startup if 'wait for network' isn't configured 
    #time.sleep(10)
    
    try:
        if config.greetingonstartup:
            start_up_print()
    except:
        log.exception('start_up_print')            
    
    try:
        process_mail()
    except:
        log.exception('process_mail')

    while True:
        time.sleep(MONITOR_POLL_PERIOD)
        try:
            monitor_mail()
        except:
            log.exception('monitor_mail')

if __name__ == '__main__':   
    try:
        logging.config.fileConfig(dir.filepath(config.logfig), disable_existing_loggers=False)
    except:        
        logging.basicConfig(level=logging.DEBUG)
        log.exception('Config Error')
        
    main()