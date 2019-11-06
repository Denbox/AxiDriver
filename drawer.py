from driver import AxiCLI
import time, math

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

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __iter__(self):
        return iter([self.x, self.y])

def circle(axi, radius, center = None):
    if center is None:
        center = axi.pos
    n_points = 128 # there's a way to compute this well - just pick the number that minimizes the step size, keeping it above the smallest step
    points = [(round(radius * math.cos(i / n_points * math.pi * 2) + center[0]), round(radius * math.sin(i / n_points * math.pi * 2) + center[1])) for i in range(n_points+1)]
    axi.pen_up()
    axi.move_to(points[0])
    axi.pen_down()
    for i in points[1:]:
        axi.move_to(i)

def spiral(axi, radius):
    # this is just like circle, except we change radius and keep spinning for longer
    # we stop when the function for radius reaches it's max
    r_steps = 512 # make this four revolutions
    n_revs = 16
    points = [(round(radius * (i / r_steps) * math.cos(i * n_revs / r_steps * math.pi * 2) + axi.pos[0]), round(radius * (i / r_steps) * math.sin(i * n_revs / r_steps * math.pi * 2) + axi.pos[1])) for i in range(r_steps)]
    axi.pen_up()
    axi.move_to(points[0])
    axi.pen_down()
    for i in points[1:]:
        axi.move_to(i)

def arc(axi, radius, theta):
    n_points = 2048
    points = [(round(radius * math.cos(i / n_points * math.pi * 2) + axi.pos[0]), round(radius * math.sin(i / n_points * math.pi * 2) + axi.pos[1])) for i in range(round(n_points * theta / math.pi / 2))]
    print(len(points))
    axi.pen_up()
    axi.move_to(points[0])
    axi.pen_down()
    for i in points[1:]:
        axi.move_to(i)

def shaded_circle(axi, max_radius, center, step=40):
    if center is None:
        center = axi.pos
    axi.pen_up()
    axi.move_to(center)
    for radius in range(step*10, max_radius, step):
        n_points = 256 # there's a way to compute this well - just pick the number that minimizes the step size, keeping it above the smallest step
        points = [(round(radius * math.cos(i / n_points * math.pi * 2) + center[0]), round(radius * math.sin(i / n_points * math.pi * 2) + center[1])) for i in range(n_points+1)]
        axi.move_to(points[0])
        axi.pen_down()
        for i in points[1:]:
            axi.move_to(i)
    axi.pen_up()

def draw_path(axi, path):
    axi.pen_up()
    axi.move_to(points_to_connect[0])
    axi.pen_down()
    for point in points_to_connect[1:]:
        axi.move_to(point)

# step size must be an integer
def snap_path_to_grid(path, step_size=50):
    gridded_path = [step_size * round(i / step_size) for i in path]
    gridded_shortened_path = [p for i, p in enumerate(gridded_path) if i == 0 or p != gridded_path[i-1]]
    return gridded_shortened_path

r = 500
n = 8192
c = Point(1000, 1000)
circle_path = [r * Point(math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n)) + c for i in range(n+1)]
gridded_circle_path = snap_path_to_grid(circle_path)
print(len(gridded_circle_path))
# axi = AxiCLI()
# center = (4000, 6000)
# # shaded_circle(axi, 500, center)
# # spiral(axi, 2000)
# # arc(axi, 3000, math.pi / 2)
# axi.pen_up()
# circle(axi, 1500, center)
# # axi.pos=(4000,4000)
# axi.close()
