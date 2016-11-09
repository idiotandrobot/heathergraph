import imaplib

def open_connection(config, verbose=False):
    
    # Connect to the server
    hostname = config.get('email', 'hostname')
    if verbose: print '++ Connecting to', hostname
    connection = imaplib.IMAP4_SSL(hostname)

    # Login to our account
    username = config.get('email', 'username')
    password = config.get('email', 'password')
    if verbose: print '++ Logging in as', username
    connection.login(username, password)
    return connection

if __name__ == '__main__':
    # Read the config file
    config = ConfigParser.ConfigParser()
    config.read([os.path.abspath('settings.ini')])

    c = open_connection(config, verbose=True)
    try:
        print c
    finally:
        c.logout()
        print "++ logged out"