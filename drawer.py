from driver import AxiCLI
import time, math, random

# no need to generalize for n dimensions, because axidraw is 2d
# maybe later if we decide to use something like paintbrushes, we can add a third dimension
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
        if isinstance(other, int) or isinstance(other, float):
            return Path([other + point for point in self.path])

        # otherwise, we want to join two paths
        return Path(self.path + other.path)

    def __radd__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Path([other + point for point in self.path])
        return Path(other.path + self.path)

    def __str__(self):
        # return '\n'.join([str(i) for i in self.path])
        return '\n'.join(map(str, self.path))

    def __round__(self):
        return Path([round(point) for point in self.path])

    def snap_to_grid(self, grid_size=8):
        self.path = grid_size * round(self / grid_size)
        # return Path(grid_size * round(self / grid_size))

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
            print(self.path[0])
            self.path.append(self.path[0])

    def draw(self, axi):
        self.snap_to_grid()
        self.prune()
        # self.path = self.prune(self.snap_to_grid())
        axi.pen_up()
        axi.move_to(tuple([*self.path[0]]))
        axi.pen_down()
        for point in self.path[1:]:
            axi.move_to(tuple([*point]))

def circle(n=None):
    if n is None:
        n = 10000
    points = [Point(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) for i in range(n+1)]
    return Path(points)

def random_circle_interior_path(radius, n=None):
    if n is None:
        n = radius // 16
    path = circle_path(radius, n=n)

def random_filled_circle_paths(radius):
    n = int(radius / 16)
    outer = radius * circle(n)
    inner = radius * circle(n)
    inner.shuffle()
    return outer, inner

paths = random_filled_circle_paths(1000)
axi = AxiCLI()
for path in paths:
    path.draw(axi)
axi.close()
