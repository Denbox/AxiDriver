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

    def __neg__(self):
        return -1 * self

    __rmul__ = __mul__
    __radd__ = __add__

    def __rsub__(self, other):
        return -(self - other)

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

def snap_path_to_grid(path, step_size=50):
    gridded_path = [step_size * round(i / step_size) for i in path]
    to_grid = lambda x: step_size * round(1.0 * x / step_size)
    new_path = [tuple(map(to_grid, point)) for point in path]
    return new_path

# axi = AxiCLI()
# center = (4000, 6000)
# # shaded_circle(axi, 500, center)
# # spiral(axi, 2000)
# # arc(axi, 3000, math.pi / 2)
# axi.pen_up()
# circle(axi, 1500, center)
# # axi.pos=(4000,4000)
# axi.close()
