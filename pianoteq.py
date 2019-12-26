from midi_shutdown_controller import MidiShutdownController
from pianoteq_controller import PianoteqController


keyboard_ports = ['.*A-PRO 1', '.*UM-ONE.*']

config = {
    # midi port to control bank/synth changes
    'bank_control.midi.ports' : keyboard_ports,
} 

pianoteq = PianoteqController()
process = pianoteq.start_async()

controller = MidiShutdownController(config)
controller.start()
