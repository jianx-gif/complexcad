import cadquery as cq
import math

plane_1 = cq.Plane(origin=(0.01636, 0.00028, -0.0675), normal=(0.0, 0.0, 1.0), xDir=(0.0, 1.0, 0.0))
sketch_1 = cq.Workplane(plane_1)
loop_1 = sketch_1.moveTo(-0.75028, 0.99636)
loop_1 = loop_1.lineTo(-0.75028, -0.96364)
loop_1 = loop_1.lineTo(-0.73028, -0.98364)
loop_1 = loop_1.lineTo(0.64306, -0.98229)
loop_1 = loop_1.threePointArc((0.72168, -0.9375), (0.7497, -0.85864))
loop_1 = loop_1.lineTo(0.74972, -0.82331)
loop_1 = loop_1.lineTo(0.74972, 0.99636)
loop_1 = loop_1.lineTo(0.72972, 1.01636)
loop_1 = loop_1.lineTo(0.09472, 1.01636)
loop_1 = loop_1.lineTo(0.07205, 0.99653)
loop_1 = loop_1.threePointArc((0.00096, 0.94138), (-0.07261, 0.99654))
loop_1 = loop_1.lineTo(-0.09528, 1.01636)
loop_1 = loop_1.lineTo(-0.73028, 1.01636)
loop_1 = loop_1.lineTo(-0.75028, 0.99636)
loop_1 = loop_1.close()
loop_2 = sketch_1.moveTo(-0.00028, 0.51636)
loop_2 = loop_2.circle(0.09999)
loop_3 = sketch_1.moveTo(-0.00028, 0.01636)
loop_3 = loop_3.circle(0.07499)
sketch_1=sketch_1.add(loop_1).add(loop_2).add(loop_3)
solid_1 = sketch_1.extrude(0.13)

result = solid_1
