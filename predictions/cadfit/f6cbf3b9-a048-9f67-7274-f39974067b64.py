import cadquery as cq
import math

# Plane definition from JSON
origin = (-0.0, 0.0, 0.0)
normal = (1.0, 0.0, 0.0)
xdir = (0.0, -1.0, 0.0)
plane_1 = cq.Plane(origin=origin, normal=normal, xDir=xdir)
sketch_1 = cq.Workplane(plane_1)

sketch_1 = sketch_1.moveTo(-0.00044, 1.0)
sketch_1 = sketch_1.lineTo(-0.73849, 0.99822)
sketch_1 = sketch_1.threePointArc((-0.78436, 0.96523), (-0.79396, 0.91329))
sketch_1 = sketch_1.lineTo(-0.79115, -1.0)
sketch_1 = sketch_1.lineTo(-0.72267, -1.0)
sketch_1 = sketch_1.lineTo(-0.71943, 0.92771)
sketch_1 = sketch_1.lineTo(-0.00044, 0.92771)
sketch_1 = sketch_1.lineTo(-0.00044, 1.0)
sketch_1 = sketch_1.close()
result = sketch_1.revolve(angleDegrees=360.0, axisStart=(0.001, 0.253, 0.001), axisEnd=(0.001, 1.253, 0.001))
