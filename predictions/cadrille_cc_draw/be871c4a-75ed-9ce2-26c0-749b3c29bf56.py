import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_edge = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_width, 0)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length)
    .lineTo(leg_width, leg_length + leg_width)
    .lineTo(leg_width, leg_length + leg_width)
    .lineTo(leg_width, leg_length)
    .lineTo(0, leg_length)
    .close()
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(leg_width/2, leg_length/2)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
combined = base.union(rib)
hole_positions = [
    (hole_offset_from_edge, leg_length/2),
    (hole_offset_from_edge, leg_length/2),
    (-hole_offset_from_edge, leg_length/2),
    (hole_offset_from_edge, leg_length/2),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
