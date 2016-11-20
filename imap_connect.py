import imaplib
import logging
log = logging.getLogger(__name__)

def open_connection(config):
    
    hostname = config.hostname
    log.info('Connecting to %s', hostname)
    connection = imaplib.IMAP4_SSL(hostname)

    username = config.username
    password = config.password
    log.info('Logging in as %s', username)
    connection.login(username, password)
    return connection