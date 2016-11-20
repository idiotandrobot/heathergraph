import os
import logging
log = logging.getLogger(__name__)

class Dir(object):

    def __init__(self, dirname):
        self.dirname = dirname
        self.path = os.path.abspath(dirname)

    def filepath(self, filename):
        value = os.path.join(self.path, filename)
        log.debug('filepath: {}'.format(value))
        return value

    def subdir(self, dirname):
        value = os.path.join(self.path, dirname)
        log.debug('subdir: {}'.format(value))
        return Dir(value)

    @staticmethod
    def root():
        value = os.path.dirname(__file__)
        log.debug('root: {}'.format(value))
        return Dir(value)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    root = Dir.root()
    root.filepath('settings.ini')
    subdir = root.subdir('subdir')
    subdir.filepath('file.txt')