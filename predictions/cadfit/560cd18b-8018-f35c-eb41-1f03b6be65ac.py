import cadquery as cq
import math

plane_1 = cq.Plane(origin=(-0.10012, 0.22791, -0.125), normal=(-0.0, -0.0, -1.0), xDir=(0.0, -1.0, 0.0))
sketch_1 = cq.Workplane(plane_1)
loop_1 = sketch_1.moveTo(0.85291, 0.86238)
loop_1 = loop_1.lineTo(0.85291, -1.06262)
loop_1 = loop_1.lineTo(0.81541, -1.10012)
loop_1 = loop_1.lineTo(-0.35959, -1.10012)
loop_1 = loop_1.lineTo(-0.39709, -1.06262)
loop_1 = loop_1.lineTo(-0.39709, 0.86238)
loop_1 = loop_1.lineTo(-0.35959, 0.89988)
loop_1 = loop_1.lineTo(0.81541, 0.89988)
loop_1 = loop_1.lineTo(0.85291, 0.86238)
loop_1 = loop_1.close()
loop_2 = sketch_1.moveTo(0.22791, -0.10012)
loop_2 = loop_2.circle(0.37495)
loop_3 = sketch_1.moveTo(-0.32209, -0.10013)
loop_3 = loop_3.circle(0.04999)
loop_4 = sketch_1.moveTo(0.77791, -0.10012)
loop_4 = loop_4.circle(0.04999)
loop_5 = sketch_1.moveTo(0.22791, -0.65012)
loop_5 = loop_5.circle(0.04999)
loop_6 = sketch_1.moveTo(0.22791, 0.44988)
loop_6 = loop_6.circle(0.04999)
sketch_1=sketch_1.add(loop_1).add(loop_2).add(loop_3).add(loop_4).add(loop_5).add(loop_6)
solid_1 = sketch_1.extrude(0.2)

result = solid_1
