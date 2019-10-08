import serial, serial.tools.list_ports
import time

# set something up so that deleting or dereferencing the object forces close
# we want this to really be the "with open() as f" type structure

class AxiCLI:
    def __init__(self, microstepping=1):
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
        self.pen_up()
        self.command('EM', 1, 1) # turn on motors with maximal microstepping

    def close(self):
        if not self.axi:
            raise RuntimeException('AxiDraw connection is already closed!')
        self.command('EM', 0, 0) # turn off motors
        self.axi.close()

    def command(self, command_word, *params):
        cmd = [command_word] + list(map(str, params)) + ['\r']
        self.axi.write(','.join(cmd).encode('utf-8'))
        return self.axi.readline().decode('utf-8').strip()

    def pen_up(self):
        self.command('SP', 1)
        time.sleep(0.4)

    def pen_down(self):
        self.command('SP', 0)
        time.sleep(0.4)

    def configure(self, MICROSTEPPING):
        self.command('EM', MICROSTEPPING, MICROSTEPPING)

    def line(self, dx, dy):
        # originally this was a constant, but doing short lines with this method causes innacuracies
        # instead, we do this magic number steps_per_ms calculation which seems to pick good speeds per line length
        # STEPS_PER_MS = 5
        steps_per_ms = int(0.004 * max(abs(dx), abs(dy)) + 1)
        duration = max(abs(dx), abs(dy)) // steps_per_ms
        self.command('XM', duration, dx, dy)
        time.sleep(duration / 1000)
