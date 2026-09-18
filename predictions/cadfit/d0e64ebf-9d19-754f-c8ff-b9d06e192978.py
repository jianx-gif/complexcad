import cadquery as cq
import math

plane_1 = cq.Plane(origin=(0.01771, -0.06322, 0.75), normal=(-0.0, -0.0, -1.0), xDir=(0.0, -1.0, 0.0))
sketch_1 = cq.Workplane(plane_1)
loop_1 = sketch_1.moveTo(-0.06324, 0.01769)
loop_1 = loop_1.circle(0.99987)
loop_2 = sketch_1.moveTo(-0.06322, 0.01771)
loop_2 = loop_2.circle(0.37495)
sketch_1=sketch_1.add(loop_1).add(loop_2)
solid_1 = sketch_1.extrude(1.5)

result = solid_1
