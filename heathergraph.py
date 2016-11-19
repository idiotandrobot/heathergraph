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

    if len(content) == 0:
        content = '++ No Potatoes Error ++'

    message = {
        'from': sender,
        'date': date,
        'subject': subject,
        'content': content
    }

    with open(dir.subdir('templates').filepath(config.template), 'r') as f:
        template = f.read()
    
    txt = template.format(**message)

    '''
    txt = ''
    txt += '-' * 32
    txt += '\r\n' * 2
    try:
        txt += 'From: %s' % sender.split()[0]
        txt += '\r\n'
    except:
        pass 
    txt += 'Date: %s' % date
    txt += '\r\n'
    txt += 'Subject: %s' % subject
    txt += '\r\n'
    txt += '* ' * 16   
    txt += '\r\n'
    if len(content) == 0: 
        txt += '++ No Potatoes Error ++'
    else:
        txt += content
    '''
    #print txt
    log.info('Message:\r\n' + txt)
    if linux_check():
        pipsta.print_to_pipsta(txt) 

def monitor_mail():
    mailbox = imap_connect.open_connection(config)
    try:
        imap_idle.monitor_folder(mailbox, config.folder, process_mail)
    finally:
        mailbox.logout()    
        
def start_up_print():
    with open(dir.subdir('templates').filepath('startup.txt'), 'r') as f:
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
    '''root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    defaultFormatter = logging.Formatter('%(asctime)s -- %(message)s')
    
    fileHandler = logging.FileHandler(dir.subdir('logs').filepath('heathergraph.log'))
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(defaultFormatter)
    root.addHandler(fileHandler)       
       
    stdoutHandler = logging.StreamHandler(sys.stdout)
    stdoutHandler.setLevel(logging.DEBUG)
    stdoutHandler.setFormatter(defaultFormatter)
    root.addHandler(stdoutHandler)'''
    
