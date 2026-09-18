import cadquery as cq
import math


# Revolve operation 1
plane_1 = cq.Plane(origin=(0.0, 0.0, -0.0), normal=(0.0, 0.0, 1.0), xDir=(0.0, 1.0, 0.0))
sketch_1 = cq.Workplane(plane_1)
sketch_1 = sketch_1.moveTo(0.9875, -0.00099)
sketch_1 = sketch_1.lineTo(0.98437, -0.99845)
sketch_1 = sketch_1.lineTo(-0.98044, -0.02491)
sketch_1 = sketch_1.lineTo(-0.24717, -0.0186)
sketch_1 = sketch_1.threePointArc((-0.182, -0.06226), (-0.12661, -0.0141))
sketch_1 = sketch_1.lineTo(0.9154, -0.00091)
sketch_1 = sketch_1.lineTo(0.9875, -0.00099)
sketch_1 = sketch_1.close()
sketch_1 = sketch_1.moveTo(-0.77861, -0.07236)
sketch_1 = sketch_1.lineTo(0.9375, -0.05514)
sketch_1 = sketch_1.lineTo(0.93481, -0.91823)
sketch_1 = sketch_1.lineTo(-0.77727, -0.07302)
sketch_1 = sketch_1.close()
solid_revolve_1 = sketch_1.revolve(angleDegrees=360.0, axisStart=(0.222, 0.001, 0.001), axisEnd=(-0.778, 0.002, 0.001))

result = solid_revolve_1