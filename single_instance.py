import os


class SingleInstance(object):
    '''
    singleinstance - based on Windows version by Dragan Jovelic this is a
                     cross-platform version that accomplishes the same task:
                     make sure that only a single instance of an application
                     is running.
    '''
    def __init__(self, pidPath='', cls=''):
        '''
        pidPath - full path/filename where pid for running application is to be
                  stored.  Often this is ./var/<pgmname>.pid
        cls     - the class object for whom a single instance is required.

        If pidPath is provided then cls is ignored
        '''
        if pidPath == '':
            if cls is not '':
                pidPath = '/var/%s.pid' % cls.__name__
            else:
                pidPath = '/var/singleinstance.pid'

        self.pidPath = pidPath
        if os.path.exists(pidPath):
            pid = open(pidPath, 'r').read().strip()
            try:
                os.kill(int(pid), 0)
                pidRunning = 1
            except OSError:
                pidRunning = 0
            if pidRunning == 1:
                self.lasterror = True
            else:
                self.lasterror = False

        else:
            self.lasterror = False

        if not self.lasterror:
            fp = open(pidPath, 'w')
            fp.write(str(os.getpid()))
            fp.close()

    def alreadyrunning(self):
        return self.lasterror

    def __del__(self):
        if not self.lasterror:
            os.unlink(self.pidPath)


class myclass(object):
    pass


def main():
    # only one instance of this script
    script_instance = SingleInstance(pidPath='/var/myscript.pid')

    if script_instance.alreadyrunning():
        print("This script is alreadyrunning")

    # In case you want single instance of only a particular class, then
    single_class = SingleInstance(cls=myclass)

    if single_class.alreadyrunning():
        print("This class already has an instance")


main()
