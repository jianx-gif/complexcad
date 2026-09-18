import cadquery as cq
leg_width = 20.0
thickness = 8.0
slot_width = 8.0
slot_spacing = 20.0
slot_depth = thickness - 2.0
hole_diameter = 6.0
csk_diameter = 12.0
csk_angle = 82.0
hole_spacing = 30.0
chamfer_size = 1.0
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_width, 0),
        (leg_width, thickness),
        (thickness, thickness),
        (thickness, leg_width),
        (0, leg_width),
        (0, 0)
    ])
    .close()
    .extrude(thickness)
)
result = (
    profile
    .faces(">Z")
    .workplane()
    .center(leg_width/2, thickness/2)
    .rect(slot_width, slot_depth)
    .cutBlind(-thickness)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(leg_width/2, thickness/2)
    .rarray(hole_spacing, 0, 2, 1)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(leg_width/2, thickness/2)
    .rarray(hole_spacing, 0, 2, 1)
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)
