import cadquery as cq
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 8.0
rib_radius = 6.0
hole_diameter = 6.0
hole_offset_x = 15.0
hole_offset_y = 10.0
slot_width = 4.0
slot_length = 12.0
slot_offset_y = 5.0
chamfer_size = 1.0
pocket_depth = 3.0
pocket_margin = 5.0
pocket_margin = 5.0
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_radius, bracket_width)
    .translate((bracket_length/2 - rib_radius, 0, 0))
    .extrude(bracket_thickness)
)
bracket = base.union(rib)
bracket = (
    bracket.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-bracket_thickness)
)
bracket = (
    bracket.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
bracket = (
    bracket.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
bracket = (
    bracket.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-bracket_thickness)
)
result = bracket
