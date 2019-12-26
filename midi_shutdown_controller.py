import sys
import time
import pexpect
from mididings import *

class MidiShutdownController(object):

    def __init__(self, config):
        self.config = config

    def start(self):
        midi_ports = self.config['bank_control.midi.ports']

        config(
            backend='alsa',
            in_ports=[
                ('midi_in',) + tuple(midi_ports)
            ]
        )

        run([
            self._shutdown_filter() >> Call(self._shutdown)
            , self._reboot_filter() >> Call(self._reboot)
        ])

    def debug(self, e):
        print e

    def _shutdown_filter(self):
        return self._two_button_filter(SYSRT_STOP, SYSRT_START)

    def _two_button_filter(self, btn1, btn2):
        class nonlocal:
            stop_t = 0
            start_t = 0

        def both_pressed(ev):
            now = time.time()
            if ((ev.type == btn1 and now - nonlocal.start_t < 0.1)
                    or (ev.type == btn2 and now - nonlocal.stop_t < 0.1)):
                return ev

            if ev.type == btn1:
                nonlocal.stop_t = now
            elif ev.type == btn2:
                nonlocal.start_t = now

            return None

        return Filter(btn1 | btn2) >> Process(both_pressed)

    def _shutdown(self, ev):
        print 'shutting down'
        print pexpect.run('sudo shutdown -P now')
        sys.exit()

    def _reboot_filter(self):
        return self._two_button_filter(SYSRT_START, SYSRT_CONTINUE)

    def _reboot(self, ev):
        print 'rebooting'
        print pexpect.run('sudo reboot')
        sys.exit()
