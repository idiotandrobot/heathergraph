import ConfigParser

class Config(object):

    def __init__(self, path):
        
        self.config = self.get_config(path)

        self.hostname = self.get_value('email', 'hostname', 'imap.gmail.com')
        self.username = self.get_value('email', 'username')
        self.password = self.get_value('email', 'password')
        self.folder = self.get_value('email', 'folder', 'Inbox')
        self.template = self.get_value('email', 'template', 'email.txt')

    @staticmethod
    def get_config(path):
        config = ConfigParser.ConfigParser()
        config.read(path)
        return config

    def get_value(self, section, key, default = None):
        try:
            return self.config.get(section, key)
        except ConfigParser.NoOptionError:
            return default

if __name__ == '__main__':
    config = Config('heathergraph.ini')
    print 'Hostname: {}'.format(config.hostname)
    print 'Username: {}'.format(config.username)
    print 'Password: {}'.format(config.password)
    print 'Folder: {}'.format(config.folder)
    print 'Template: {}'.format(config.template)