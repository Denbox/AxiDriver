from driver import AxiCLI
import math

axi = AxiCLI()
n_points = 128
radius = 2000

points = [(round(radius * math.cos(i / n_points * math.pi * 2)), round(radius * math.sin(i / n_points * math.pi * 2))) for i in range(n_points+1)]

# we start and end at (0, 0). so the edges to travel are the differences between
# points + [(0, 0)] and [(0, 0)] + points
ends   = points + [(0, 0)]
starts = [(0, 0)] + points
edges = [(ends[i][0] - starts[i][0], ends[i][1] - starts[i][1]) for i in range(len(ends))]

axi.line(*edges[0])
axi.pen_down()
for i in range(1, len(edges)-1):
    axi.line(*edges[i])
axi.pen_up()
axi.line(*edges[-1])

axi.close()
