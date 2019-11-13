from driver import AxiCLI, Path, Point
import time, math, random

# no need to generalize for n dimensions, because axidraw is 2d
# maybe later if we decide to use something like paintbrushes, we can add a third dimension
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

paths = random_filled_circle_paths(400)
axi = AxiCLI()
for path in paths:
    axi.draw(path)
axi.close()
