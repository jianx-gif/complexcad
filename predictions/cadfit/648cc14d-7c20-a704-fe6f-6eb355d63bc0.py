import cadquery as cq
import math

plane_1 = cq.Plane(origin=(-0.01762, 0.35783, 0.25177), normal=(0.0, -1.0, -0.0), xDir=(-1.0, -0.0, 0.0))
sketch_1 = cq.Workplane(plane_1)
loop_1 = sketch_1.moveTo(0.9788, 0.09483)
loop_1 = loop_1.lineTo(0.97876, -0.09833)
loop_1 = loop_1.lineTo(-0.9456, -0.09833)
loop_1 = loop_1.lineTo(-0.9456, 0.09483)
loop_1 = loop_1.lineTo(0.97876, 0.09483)
loop_1 = loop_1.close()
sketch_1=sketch_1.add(loop_1)
solid_1 = sketch_1.extrude(0.72)

result = solid_1