import cadquery as cq
import math
module = 2.0
module = 2.0
module = 2.0
module = 1.0
outer_radius = 30.0
inner_radius = 20.0
lip_thickness = 2.0
lip_height = 10.0
pilot_diameter = 5.0
chamfer_len = 2.0
pocket_height = 8.0
pocket_depth = module * module
profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (module, 0),
        (module, module),
        (module, module),
        (module, module),
        (0, module),
    ])
    .close()
)
mod = profile.revolve()
mod = mod.edges().chamfer(chamfer_len)
pocket = (
    cq.Workplane("XY")
    .circle(module)
    .extrude(module)
)
pocket = (
    pocket.faces(">Z")
    .workplane()
    .circle(pilot_diameter / 2)
    .extrude(pocket_height)
)
pocket = pocket.cut(pocket)
result = (
    pocket
    .faces(">Z")
    .workplane()
    .hole(pilot_diameter, module)
)
