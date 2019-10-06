import serial, serial.tools.list_ports
import time

# in github mention things used from fogleman!
# basically copied his command function
# and his configuration settings (is this from regular axidraw?)
# and also learned from his error correction

class AxiCLI:
    def __init__(self):
        self.port_connector = self.fetch_port()
        self.axi = None
        self.open()

    # if axidraw is connected, this returns the port to connect to
    # if multiple axidraws are connected, this picks the first one - sorry!
    def fetch_port(self):
        for port in serial.tools.list_ports.comports():
            port_connector = port[0]
            port_name     = port[1]
            if 'EiBotBoard' in port_name:
                return port_connector
        raise EnvironmentError('Can\'t find an AxiDraw!')

    def open(self):
        if self.axi:
            raise RuntimeException('AxiDraw connection is already open!')
        self.axi = serial.Serial(self.port_connector, timeout=1)
        self.axi.reset_input_buffer()

    def close(self):
        if not self.axi:
            raise RuntimeException('AxiDraw connection is already closed!')
        self.axi.close()

    def command(self, command_word, *params):
        cmd = [command_word] + list(map(str, params)) + ['\r']
        self.axi.write(','.join(cmd).encode('utf-8'))

    def pen_up(self):
        self.command('SP', 1)

    def pen_down(self):
        self.command('SP', 0)


axi = AxiCLI()
# axi.command('TP')
axi.pen_down()
axi.close()
