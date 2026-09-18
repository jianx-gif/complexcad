import cadquery as cq
import math

plane_1 = cq.Plane(origin=(-0.5, 0.15207, -0.03884), normal=(1.0, 0.0, -0.0), xDir=(0.0, -1.0, 0.0))
sketch_1 = cq.Workplane(plane_1)
loop_1 = sketch_1.moveTo(1.15207, 0.14866)
loop_1 = loop_1.lineTo(1.15207, -0.05134)
loop_1 = loop_1.lineTo(-0.09793, -0.05134)
loop_1 = loop_1.lineTo(-0.09793, -0.22634)
loop_1 = loop_1.lineTo(-0.84793, -0.22634)
loop_1 = loop_1.lineTo(-0.84793, 0.14866)
loop_1 = loop_1.lineTo(1.13046, 0.14866)
loop_1 = loop_1.lineTo(1.15207, 0.14866)
loop_1 = loop_1.close()
sketch_1=sketch_1.add(loop_1)
solid_1 = sketch_1.extrude(1.0)

result = solid_1
