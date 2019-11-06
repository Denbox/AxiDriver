import serial, serial.tools.list_ports
import time

# set something up so that deleting or dereferencing the object forces close
# we want this to really be the "with open() as f" type structure

def point_sum(a, b):
    return (a[0] + b[0], a[1] + b[1])

def point_diff(a, b):
    return point_sum(a, (-b[0], -b[1]))

class AxiCLI:
    def __init__(self, microstepping=1):
        self.port_connector = self.fetch_port()
        self.axi = None
        self.open()
        self.pos = (0, 0)

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
        time.sleep(0.1)
        self.pen_up()
        self.move_to((0, 0))
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

    def line(self, move):
        STEPS_PER_MS = 2
        duration = max(map(abs, move)) // STEPS_PER_MS
        self.command('XM', duration, *move)
        time.sleep(duration / 1000)
        self.pos = point_sum(self.pos, move)

    def move_to(self, pos):
        move = point_diff(pos, self.pos)
        self.line(move)
