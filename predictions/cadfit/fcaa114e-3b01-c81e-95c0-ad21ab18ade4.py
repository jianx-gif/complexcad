import cadquery as cq
import math

# Plane definition from JSON
origin = (0.0, -0.0, 0.0)
normal = (0.0, 1.0, 0.0)
xdir = (1.0, 0.0, 0.0)
plane_1 = cq.Plane(origin=origin, normal=normal, xDir=xdir)
sketch_1 = cq.Workplane(plane_1)

sketch_1 = sketch_1.moveTo(-0.88216, 0.78166)
sketch_1 = sketch_1.lineTo(-0.85908, 0.78092)
sketch_1 = sketch_1.lineTo(-0.84866, 0.7705)
sketch_1 = sketch_1.lineTo(-0.85091, -0.55743)
sketch_1 = sketch_1.threePointArc((-0.8547, -0.57085), (-0.86094, -0.58273))
sketch_1 = sketch_1.threePointArc((-0.90699, -0.6775), (-0.95688, -0.77395))
sketch_1 = sketch_1.lineTo(-0.97256, -0.78166)
sketch_1 = sketch_1.lineTo(-0.99383, -0.78166)
sketch_1 = sketch_1.lineTo(-0.99967, -0.77063)
sketch_1 = sketch_1.threePointArc((-0.9454, -0.66506), (-0.89575, -0.56248))
sketch_1 = sketch_1.threePointArc((-0.89413, -0.55184), (-0.89313, -0.54284))
sketch_1 = sketch_1.lineTo(-0.89035, 0.77347)
sketch_1 = sketch_1.close()
result = sketch_1.revolve(angleDegrees=360.0, axisStart=(0.001, -0.016999999999999998, 0.001), axisEnd=(0.001, 0.983, 0.001))
