import cadquery as cq
import math


# Revolve operation 1
plane_1 = cq.Plane(origin=(-0.0, 0.0, 0.0), normal=(1.0, 0.0, 0.0), xDir=(0.0, -1.0, 0.0))
sketch_1 = cq.Workplane(plane_1)
sketch_1 = sketch_1.moveTo(-0.55, 0.99969)
sketch_1 = sketch_1.lineTo(-0.65105, 0.99864)
sketch_1 = sketch_1.lineTo(-0.66667, 0.98303)
sketch_1 = sketch_1.lineTo(-0.66454, 0.21448)
sketch_1 = sketch_1.threePointArc((-0.65665, 0.20649), (-0.64996, 0.19998))
sketch_1 = sketch_1.lineTo(0.65306, 0.203)
sketch_1 = sketch_1.lineTo(0.66667, 0.2166)
sketch_1 = sketch_1.lineTo(0.66565, 0.31758)
sketch_1 = sketch_1.lineTo(0.65, 0.33323)
sketch_1 = sketch_1.lineTo(-0.51972, 0.33628)
sketch_1 = sketch_1.lineTo(-0.53333, 0.34989)
sketch_1 = sketch_1.lineTo(-0.5354, 0.98509)
sketch_1 = sketch_1.lineTo(-0.54895, 0.99864)
sketch_1 = sketch_1.close()
solid_revolve_1 = sketch_1.revolve(angleDegrees=360.0, axisStart=(-0.187, 0.001, 0.001), axisEnd=(0.8130000000000001, 0.002, 0.001))

result = solid_revolve_1