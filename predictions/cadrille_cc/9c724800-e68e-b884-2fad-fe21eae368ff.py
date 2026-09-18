import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 10.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
hole_offset = 15.0
hole_offset = 15.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_length, 0)
    .lineTo(leg_length, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(0, leg_length)
    .close()
    .extrude(thickness)
)
result = base.union(leg)
result = (
    result.faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
