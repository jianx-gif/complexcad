import cadquery as cq
import math

plane_1 = cq.Plane(origin=(-1.0, 0.0, 0.0), normal=(1.0, 0.0, 0.0), xDir=(0.0, -1.0, 0.0))
sketch_1 = cq.Workplane(plane_1)
loop_1 = sketch_1.moveTo(0.75, 0.15)
loop_1 = loop_1.lineTo(0.74819, -0.12681)
loop_1 = loop_1.lineTo(0.725, -0.15)
loop_1 = loop_1.lineTo(0.25, -0.14744)
loop_1 = loop_1.lineTo(0.24874, -0.05)
loop_1 = loop_1.lineTo(-0.25, -0.05256)
loop_1 = loop_1.lineTo(-0.25125, -0.15)
loop_1 = loop_1.lineTo(-0.72672, -0.14828)
loop_1 = loop_1.lineTo(-0.75, -0.125)
loop_1 = loop_1.lineTo(-0.74876, 0.15)
loop_1 = loop_1.lineTo(0.74874, 0.15)
loop_1 = loop_1.close()
sketch_1=sketch_1.add(loop_1)
solid_1 = sketch_1.extrude(2.0)

result = solid_1
