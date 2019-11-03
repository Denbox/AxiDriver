from driver import AxiCLI
import time, math

def circle(axi, radius):
    n_points = 256 # there's a way to compute this well - just pick the number that minimizes the step size, keeping it above the smallest step
    points = [(round(radius * math.cos(i / n_points * math.pi * 2) + axi.pos[0]), round(radius * math.sin(i / n_points * math.pi * 2) + axi.pos[1])) for i in range(n_points+1)]
    axi.pen_up()
    axi.move_to(points[0])
    axi.pen_down()
    for i in points[1:]:
        axi.move_to(i)

def spiral(axi, radius):
    # this is just like circle, except we change radius and keep spinning for longer
    # we stop when the function for radius reaches it's max
    r_steps = 8192 # make this four revolutions
    n_revs = 32
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

axi = AxiCLI()
axi.move_to((4000, 4000))
# circle(axi, 1000)
spiral(axi, 2000)
# arc(axi, 3000, math.pi / 2)
axi.pen_up()
# axi.pos=(4000,4000)
axi.close()
