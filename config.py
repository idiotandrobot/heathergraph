import ConfigParser
import getpass
import logging
log = logging.getLogger(__name__)

class Config(object):

    def __init__(self, path):
        
        self.path = path
        self.config = self.get_config(path)
        # email
        self.hostname = self.get_value('email', 'hostname', 'imap.gmail.com')
        self.username = self.get_value('email', 'username')
        self.password = self.get_value('email', 'password')
        self.folder = self.get_value('email', 'folder', 'Inbox')
        # print
        self.greetingonstartup = bool(self.get_boolvalue('print', 'greetingonstartup', True))
        self.startuptemplate = self.get_value('print', 'startuptemplate', 'startup.txt')
        self.template = self.get_value('print', 'template', 'email.txt')
        # logging
        self.logfig = self.get_value('logging', 'config', 'logging.ini')
        # encoding
        self.encodingerrors = self.get_value('encoding', 'errors', 'replace')

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
        except ConfigParser.NoOptionError as err:
            if default == None:
                raise err
            return default
    
    # separate logging of values to deal with likelyhood 
    # logging may not be initialised when config loaded
    def log_values(self):
        log_value = log.info
        log_value('Config: {}'.format(self.path))
        # email
        log_value('Hostname: {}'.format(self.hostname))    
        log_value('Username: {}'.format(self.username))            
        log_value('Password: ********')
        log_value('Folder: {}'.format(self.folder))
        # print
        log_value('Greeting on Startup: {}'.format(self.greetingonstartup))    
        log_value('Startup Template: {}'.format(self.startuptemplate))
        log_value('Template: {}'.format(self.template))    
        # logging
        log_value('Logfig: {}'.format(self.logfig))
        # encoding
        log_value('Encoding Errors: {}'.format(self.encodingerrors))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    config = Config('heathergraph.ini')
    config.log_values()
    