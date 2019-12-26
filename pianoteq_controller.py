import sys
import pexpect

class PianoteqController(object):

    def start_async(self):
        command = '/home/pi/pianoteq/Pianoteq\ 6\ STAGE --multicore max --headless --midimapping \'Minimalistic (custom)\''
        print 'starting pianoteq'
        process = pexpect.spawn(command)
        print process
        process.logfile = sys.stdout
        return process
