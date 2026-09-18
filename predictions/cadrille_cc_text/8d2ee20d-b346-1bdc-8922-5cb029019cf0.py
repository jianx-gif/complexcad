import cadquery as cq
import math
gear_outer_radius = 50.0
gear_inner_radius = 30.0
gear_thickness = 15.0
pinion_radius = 20.0
pinion_height = 5.0
pinion_count = 6
pinion_radius = 30.0
tooth_height = 5.0
tooth_width = tooth_height * 0.6
tooth_depth = gear_thickness * 0.6
hole_diameter = 5.0
hole_count = 4
hole_spacing = (gear_outer_radius - tooth_width) / (tooth_width - tooth_height)
base = (
    cq.Workplane("XY")
    .circle(gear_outer_radius)
    .extrude(gear_thickness)
)
base = base.edges().chamfer(chamfer_size)
pinion = (
    cq.Workplane("XY")
    .circle(pinion_radius)
    .extrude(pinion_height)
)
pinion = (
    cq.Workplane("XY")
    .circle(pinion_radius)
    .extrude(pinion_height)
)
pinion = (
    cq.Workplane("XY")
    .rect(pinion_radius, pinion_height)
    .extrude(pinion_height)
)
pinion = pin Join.union(pinion)
pinion = pining.cut(pinion)
pinion = (
    pining
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)
pinson = pining
pinson = pining
pinson = pining
pinson = pining
pinson = pinson[0]])
pinson = pining
pinson = pining
pinson = pining
pinson = pining
pinson = pining
pinson = pining
pinson = pining
pinson = pining
pinson = pining
pinson = pining
pinson = pinson.pinson[1])
pinson = pinface(pinson[1])]
pinson = pining[1) if pinson(pinson[1]]])
pinson = pining[1][-pinson[1], pinson[10, pinson[10)]
pinson = pinface(pinson[1], pinson[10)]
pinson = pinface(pinson[1], pinson[10)]
pinson = pin[0] - pinson(pinson[1], pinson[10)]
pinson = pin[0] - pinson[1], pinson[10)]
pinson = pin[0] - pinson[1], pinson[1]]
pinson = pin[0] - pinson[1], pinson[1]]
pinson = pin[0] - pinson[1], pinson[1]]
pinson = pin[0] + pinson(pinson[1], pinson[10)]
pinson = pin[0] + pinson[1], pinson[10)]
pinson = pin[0] + pinson[1], pinson[10)]
pinson = pin[0] + pinson[1], pinson[10)]
pinson = pin[0] + pinson[1], pinson[10)]
pinson = pin[0] + pinson[1], pinson[10)]
pinson = pin[0] + pinson[1], pinson[10)]
pinson = pin[0] + pinson[1], pinson[10)]
pinson = pin[0] + pinson[1], pinson[10)]
pinson = pin.revolve(2)
pinson = pin.revolve(2)
pinson = pin.revolve(2)
pinson = pin.revolve(2)
pinson = pin.revolve(2)
pinson = pin.revolve(2)
pinson = pin.revolve(2)
pinson = pin.revolve(2)
pinson = pin.revolve(2)
pinson = pin.revolve(2)
pinson = pin.revolve(2)
pinson = pin.revolve(2)
pinson