import cadquery as cq

bracket_length = 80.0
bracket_width = 50.0
bracket_thickness = 8.0
pocket_width = 20.0
pocket_height = 10.0
pocket_depth = 4.0
pocket_offset_y = 15.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset_y = 20.0
chamfer_size = 1.0
rib_thickness = 3.0
rib_height = 12.0
rib_length = bracket_length - 20.0

base = (
    cq.Workplane("XY")
    .rect(bracket_width, bracket_length)
    .extrude(bracket_thickness)
)

base = base.edges("|Z").chamfer(chamfer_size)

pocket = (
    base.faces(">Z")
    .workplane()
    .center(0, pocket_offset_y)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)

holes = (
    pocket.faces(">Z")
    .workplane()
    .center(-hole_spacing/2, hole_offset_y)
    .hole(hole_diameter)
    .center(hole_spacing, 0)
    .hole(hole_diameter)
)

rib_left = (
    holes.faces("<X")
    .workplane()
    .rect(rib_thickness, rib_length)
    .extrude(rib_height)
)

rib_right = (
    holes.faces(">X")
    .workplane()
    .rect(rib_thickness, rib_length)
    .extrude(-rib_height)
)

result = holes.union(rib_left).union(rib_right)
