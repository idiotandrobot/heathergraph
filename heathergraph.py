import argparse
import platform
import signal
import sys
import time
import ConfigParser
import os
import imaplib
import imap_connect
import imap_read
import imap_idle
from throttle import throttle

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
    config = ConfigParser.ConfigParser()
    config.read([os.path.abspath('settings.ini')])

    mailbox = imap_connect.open_connection(config, verbose=True)
    try:
        imap_read.read_folder(mailbox, config.get('email', 'folder'))
    finally:
        mailbox.logout()

def monitor_mail():
    config = ConfigParser.ConfigParser()
    config.read([os.path.abspath('settings.ini')])

    mailbox = imap_connect.open_connection(config, verbose=True)
    try:
        imap_idle.monitor_folder(mailbox, config.get('email', 'folder'), \
        process_mail)
    finally:
        mailbox.logout()    

def main():
    if platform.system() != 'Linux':
        print 'This script has only been written for Linux'
        #sys.exit('This script has only been written for Linux')
    
    parse_arguments()
        
    signal.signal(signal.SIGINT, signal_handler)    

    process_mail()

    while True:
        time.sleep(MONITOR_POLL_PERIOD)
        monitor_mail()

if __name__ == '__main__':
    main()
