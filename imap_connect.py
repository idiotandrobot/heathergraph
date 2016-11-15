import imaplib
import logging
log = logging.getLogger(__name__)

def open_connection(config, verbose=False):
    
    # Connect to the server
    hostname = config.hostname
    #if verbose: print '++ Connecting to', hostname
    log.debug('Connecting to %s', hostname)
    connection = imaplib.IMAP4_SSL(hostname)

    # Login to our account
    username = config.username
    password = config.password
    #if verbose: print '++ Logging in as', username
    log.debug('Logging in as %s', username)
    connection.login(username, password)
    return connection