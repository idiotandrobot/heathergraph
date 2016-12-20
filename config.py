import ConfigParser
import getpass
import logging
log = logging.getLogger(__name__)

class Config(object):

    def __init__(self, path):
        
        self.config = self.get_config(path)
        log.debug('Config: {}'.format(path))
        self.hostname = self.get_value('email', 'hostname', 'imap.gmail.com')
        log.debug('Hostname: {}'.format(self.hostname))    
        self.username = self.get_value('email', 'username')
        log.debug('Username: {}'.format(self.username))            
        self.password = self.get_value('email', 'password')
        log.debug('Password: ********')
        self.folder = self.get_value('email', 'folder', 'Inbox')
        log.debug('Folder: {}'.format(self.folder))
        self.greetingonstartup = bool(self.get_boolvalue('print', 'greetingonstartup', True))
        log.debug('Greeting on Startup: {}'.format(self.greetingonstartup))    
        self.template = self.get_value('print', 'template', 'email.txt')
        log.debug('Template: {}'.format(self.template))    
        self.logfig = self.get_value('logging', 'config', 'logging.ini')
        log.debug('Logfig: {}'.format(self.logfig))

    @staticmethod
    def get_config(path):
        config = ConfigParser.ConfigParser()
        config.read(path)
        return config

    def get_boolvalue(self, section, key, default = False):
        try:
            return self.config.getboolean(section, key)
        except ConfigParser.NoSectionError:
            return default
        except ConfigParser.NoOptionError:
            return default

    def get_value(self, section, key, default = None):
        try:
            return self.config.get(section, key)
        except ConfigParser.NoSectionError:
            return default
        except ConfigParser.NoOptionError:
            return default

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    config = Config('heathergraph.ini')
    