import os

class Dir(object):

    def __init__(self, dirname):
        self.dirname = dirname

    def path(self):
        return os.path.abspath(self.dirname)

    def filepath(self, filename):
        return(os.path.join(self.path(), filename))

    def subdir(self, dirname):
        return Dir(self.filepath(dirname))

    @staticmethod
    def root():
        return Dir(os.path.dirname(__file__))


if __name__ == '__main__':
    root = Dir.root()
    print root.path()
    print root.filepath('settings.ini')
    print root.subdir('subdir').path()
    print root.subdir('subdir').filepath('file.txt')