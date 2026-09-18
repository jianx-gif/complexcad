import cadquery as cq

bracket_base_width = 80.0
bracket_base_height = 50.0
bracket_top_width = 60.0
bracket_top_height = 30.0
loft_length = 30.0
pocket_width = 30.0
pocket_height = 20.0
pocket_depth = 8.0
hole_clearance_diameter = 7.0
hole_spacing = 40.0
chamfer_distance = 0.5

base_wire = cq.Workplane("XY").rect(bracket_base_width, bracket_base_height).wire()
result = (
    base_wire
    .workplane(offset=loft_length)
    .rect(bracket_top_width, bracket_top_height)
    .wire()
    .loft()
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-hole_spacing/2, 0)
    .hole(hole_clearance_diameter)
    .center(hole_spacing, 0)
    .hole(hole_clearance_diameter)
)
result = result.edges("|Z").chamfer(chamfer_distance)
