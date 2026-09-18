import cadquery as cq
import math


# Revolve operation 1
plane_1 = cq.Plane(origin=(-0.0, 0.0, 0.0), normal=(1.0, 0.0, 0.0), xDir=(0.0, -1.0, 0.0))
sketch_1 = cq.Workplane(plane_1)
sketch_1 = sketch_1.moveTo(-0.01895, 0.87876)
sketch_1 = sketch_1.threePointArc((0.06675, 0.81055), (0.1583, 0.7588))
sketch_1 = sketch_1.threePointArc((0.26095, 0.71571), (0.3622, 0.68438))
sketch_1 = sketch_1.threePointArc((0.39276, 0.67586), (0.42155, 0.66925))
sketch_1 = sketch_1.lineTo(0.53367, 0.6447)
sketch_1 = sketch_1.threePointArc((0.55901, 0.64067), (0.58409, 0.63483))
sketch_1 = sketch_1.lineTo(0.67112, 0.62275)
sketch_1 = sketch_1.threePointArc((0.71554, 0.61687), (0.75995, 0.60623))
sketch_1 = sketch_1.lineTo(0.79263, 0.59517)
sketch_1 = sketch_1.threePointArc((0.80842, 0.58725), (0.82332, 0.58136))
sketch_1 = sketch_1.threePointArc((0.83617, 0.57163), (0.84877, 0.56466))
sketch_1 = sketch_1.threePointArc((0.86528, 0.54836), (0.87738, 0.5287))
sketch_1 = sketch_1.threePointArc((0.87666, 0.50718), (0.86263, 0.49101))
sketch_1 = sketch_1.threePointArc((0.84672, 0.48174), (0.82963, 0.47601))
sketch_1 = sketch_1.threePointArc((0.79348, 0.468), (0.75619, 0.46389))
sketch_1 = sketch_1.threePointArc((0.6381, 0.45936), (0.51601, 0.45932))
sketch_1 = sketch_1.threePointArc((0.30135, 0.46011), (0.09619, 0.46005))
sketch_1 = sketch_1.threePointArc((-0.10576, 0.46121), (-0.31511, 0.46434))
sketch_1 = sketch_1.threePointArc((-0.35871, 0.46707), (-0.40274, 0.47329))
sketch_1 = sketch_1.threePointArc((-0.41063, 0.47598), (-0.41847, 0.47925))
sketch_1 = sketch_1.lineTo(-0.0195, 0.87822)
sketch_1 = sketch_1.close()
solid_revolve_1 = sketch_1.revolve(angleDegrees=360.0, axisStart=(-0.184, 0.186, 0.001), axisEnd=(0.523, -0.522, 0.001))

result = solid_revolve_1