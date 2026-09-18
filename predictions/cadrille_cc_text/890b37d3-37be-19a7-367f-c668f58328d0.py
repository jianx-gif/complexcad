import cadquery as cq
panel_width = 100.0
panel_height = 80.0
panel_thickness = 4.0
border_chamfer = 2.0
slot_length = 20.0
slot_width = 4.0
slot_spacing = 12.0
hole_diameter = 6.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing = 20.0
base = (
    cq.Workplane("XY")
    .rect(panel_width, panel_height)
    .extrude(panel_thickness)
)
slot_center_x = -panel_width/2 + slot_spacing/2
slot_center_y = -panel_height/2 + slot_spacing/2
result = (
    base
    .faces(">Z")
    .workplane()
    .center(slot_center_x, slot_center_y)
    .rect(slot_length, slot_width)
    .cutBlind(-panel_thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_spacing/2, 0)
    .hole(hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_spacing, 0)
    .hole(hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_spacing, 0)
    .hole(hole_diameter)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_spacing, 0)
    .hole(hole_diameter)
)
