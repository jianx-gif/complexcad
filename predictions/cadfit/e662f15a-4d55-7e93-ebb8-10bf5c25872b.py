import cadquery as cq
import math

plane_1 = cq.Plane(origin=(-0.99, 0.0, 0.0), normal=(1.0, 0.0, 0.0), xDir=(0.0, -1.0, 0.0))
sketch_1 = cq.Workplane(plane_1)
loop_1 = sketch_1.moveTo(0.5, 0.1875)
loop_1 = loop_1.lineTo(0.49878, -0.14845)
loop_1 = loop_1.threePointArc((0.47806, -0.17883), (0.44107, -0.18696))
loop_1 = loop_1.lineTo(-0.46241, -0.18593)
loop_1 = loop_1.threePointArc((-0.49191, -0.16469), (-0.49947, -0.12856))
loop_1 = loop_1.lineTo(-0.49819, 0.1875)
loop_1 = loop_1.lineTo(0.4991, 0.1875)
loop_1 = loop_1.close()
sketch_1=sketch_1.add(loop_1)
solid_1 = sketch_1.extrude(1.98)

result = solid_1
