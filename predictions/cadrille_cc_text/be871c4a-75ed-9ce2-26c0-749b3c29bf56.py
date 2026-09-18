import cadquery as cq
horizontal_leg_length = 70.0
vertical_leg_length = vertical_leg_length
leg_thickness = 8.0
leg_width = 20.0
fillet_radius = 3.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset_from_base = 20.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_thickness, 0),
        (leg_thickness, leg_width),
        (leg_width, leg_width),
        (leg_width, leg_thickness),
        (0, leg_thickness),
        (0, 0)
    ])
    .close()
    .extrude(leg_thickness)
)
result = base.edges("|Z").fillet(fillet_radius)
result = (
    result.faces(">Z")
    .workplane()
    .center(hole_offset_from_base, hole_offset_from_base)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(hole_offset_from_base, hole_offset_from_base)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(hole_offset_from_base, hole_offset_from_base)
    .hole(hole_diameter)
)
