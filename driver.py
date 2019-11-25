import serial, serial.tools.list_ports
import time, random, math

# set something up so that deleting or dereferencing the object forces close
# we want this to really be the "with open() as f" type structure

class AxiCLI:
    def __init__(self, microstepping=1):
        self.port_connector = self.fetch_port()
        self.axi = None
        self.open()
        self.pos = Point(0, 0)

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
        self.move_to(Point(0, 0))
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

    def line(self, move, steps_per_ms=2):
        duration = max(map(abs, move)) // steps_per_ms
        self.command('XM', duration, *move)
        time.sleep(duration / 1000)
        self.pos += move

    def move_to(self, pos, steps_per_ms=2):
        move = pos - self.pos
        self.line(move, steps_per_ms=steps_per_ms)

    def draw(self, path, in_place = True, steps_per_ms = 2):
        # in place means we draw the path from our current position
        # rather than the absolute coordinate information from path
        start = self.pos
        if in_place:
            path += self.pos
        path.snap_to_grid()
        path.prune()
        self.pen_up()
        self.move_to(path[0], steps_per_ms=steps_per_ms)
        self.pen_down()
        for point in path[1:]:
            self.move_to(point, steps_per_ms=steps_per_ms)
        self.pen_up()
        self.move_to(start, steps_per_ms=steps_per_ms)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __round__(self):
        return Point(round(self.x), round(self.y))

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Point(self.x + other, self.y + other)
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Point(self.x * other, self.y * other)
        return Point(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Point(self.x / other, self.y / other)
        return Point(self.x / other.x, self.y / other.y)

    __rmul__ = __mul__
    __radd__ = __add__

    def __rsub__(self, other):
        return -(self - other)

    def __rtruediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Point(other / self.x, other / self.y)
        return Point(other.x / self.x, other.y / self.y)

    def __neg__(self):
        return -1 * self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __list__(self):
        return [self.x, self.y]

    def __tuple(self):
        return (self.x, self.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __iter__(self):
        return iter([self.x, self.y])

class Path:
    def __init__(self, points):
        self.path = points
        if self.path == []:
            raise ValueError('Empty Path!')
        if not all(isinstance(i, Point) for i in self.path):
            raise ValueError('Non Point Types in Path!')

    def __mul__(self, scalar):
        return Path([scalar * point for point in self.path])

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return Path([point / scalar for point in self.path])

    def __add__(self, other):
        # we want to shift our path
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, Point):
            return Path([other + point for point in self.path])

        # otherwise, we want to join two paths
        return Path(self.path + other.path)

    def __radd__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Path([other + point for point in self.path])
        return Path(other.path + self.path)

    def __str__(self):
        return '\n'.join(map(str, self.path))

    def __round__(self):
        return Path([round(point) for point in self.path])

    def snap_to_grid(self, grid_size=8):
        self.path = grid_size * round(self / grid_size)

    def __getitem__(self, key):
        return self.path[key]

    # remove duplicate elements in path
    def prune(self):
        # start with first element
        # only add new elements if they differ from the most recent one
        new_path = [self.path[0]]
        for point in self.path[1:]:
            if point != new_path[-1]:
                new_path.append(Point(*point))
        self.path = new_path

    def shuffle(self, closed=True):
        random.shuffle(self.path)
        if closed:
            self.path.append(self.path[0])
