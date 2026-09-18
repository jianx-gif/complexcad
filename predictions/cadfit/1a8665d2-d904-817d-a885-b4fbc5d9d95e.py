import cadquery as cq
import math

# Plane definition from JSON
origin = (-0.0, 0.0, 0.0)
normal = (1.0, 0.0, 0.0)
xdir = (0.0, -1.0, 0.0)
plane_1 = cq.Plane(origin=origin, normal=normal, xDir=xdir)
sketch_1 = cq.Workplane(plane_1)

sketch_1 = sketch_1.moveTo(-0.44431, 0.22222)
sketch_1 = sketch_1.lineTo(-0.99969, 0.22074)
sketch_1 = sketch_1.lineTo(-0.99821, -0.22222)
sketch_1 = sketch_1.lineTo(-0.44431, -0.22074)
sketch_1 = sketch_1.lineTo(-0.44357, -0.15556)
sketch_1 = sketch_1.lineTo(-0.33323, -0.15481)
sketch_1 = sketch_1.lineTo(-0.33397, 0.15556)
sketch_1 = sketch_1.lineTo(-0.44431, 0.1563)
sketch_1 = sketch_1.lineTo(-0.44431, 0.22148)
sketch_1 = sketch_1.close()
result = sketch_1.revolve(angleDegrees=360.0, axisStart=(0.001, 0.001, 0.001), axisEnd=(0.001, 1.001, 0.001))
