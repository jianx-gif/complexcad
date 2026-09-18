import cadquery as cq
import math
num_teeth = 20
num_teeth = 30
num_teeth = 24
base = cq.Workplane('XY').rect(80,20).extrude(2)
result = base.edges().chamfer(1)
