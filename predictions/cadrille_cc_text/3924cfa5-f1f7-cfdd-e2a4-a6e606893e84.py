import cadquery as cq
bracket_base_width = 80.0
bracket_top_width = 60.0
bracket_top_height = 50.0
bracket_top_height = 30.0
pocket_width = 30.0
pocket_height = 20.0
pocket_depth = 8.0
hole_clearance_diameter = 7.0
hole_spacing = 40.0
chamfer_distance = 0.5
base = (
    cq.Workplane("XY")
    .rect(bracket_base_width, bracket_top_height)
    .extrude(bracket_top_height)
)
pocket = (
    base.faces(">Z").workplane()
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)
pocket = (
    pocket.faces(">Z").workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)
result = base.union(pocket)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .hole(hole_clearance_diameter)
)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .hole(hole_clearance_diameter)
)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .hole(hole_clearance_diameter)
)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .hole(hole_clearance_diameter)
)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)
