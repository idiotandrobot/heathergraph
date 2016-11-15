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

    #print txt
    log.debug(txt)
    if linux_check():
        pipsta.print_to_pipsta(txt) 

def monitor_mail():
    mailbox = imap_connect.open_connection(config)
    try:
        imap_idle.monitor_folder(mailbox, config.folder, process_mail)
    finally:
        mailbox.logout()    
        
def start_up_print():
    txt = '+ ' * 16 + '\r\n' + ' ' * 13 + 'Hello\r\n' + '+ ' * 16
    log.debug(txt)
    if linux_check():
        pipsta.print_to_pipsta(txt)


def main():
    parse_arguments()
        
    signal.signal(signal.SIGINT, signal_handler)    

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
    
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    defaultFormatter = logging.Formatter('%(asctime)s -- %(message)s')
    
    fileHandler = logging.FileHandler(dir.subdir('logs').filepath('heathergraph.log'))
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(defaultFormatter)
    root.addHandler(fileHandler)       
       
    stdoutHandler = logging.StreamHandler(sys.stdout)
    stdoutHandler.setLevel(logging.DEBUG)
    stdoutHandler.setFormatter(defaultFormatter)
    root.addHandler(stdoutHandler)
    
    main()
