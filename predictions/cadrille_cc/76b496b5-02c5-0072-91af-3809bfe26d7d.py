import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 10.0
fillet_radius = 2.0
hole_diameter = 6.0
hole_spacing = 12.0
hole_offset = 10.0
chamfer_size = 0.5
rib_width = 4.0
rib_height = 10.0
rib_thickness = 4.0
rib_spacing = 12.0
rib_count = 4
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_length, 0),
        (leg_length, leg_width),
        (leg_width, leg_width),
        (leg_width, leg_width),
        (0, leg_width),
    ])
    .close()
    .extrude(thickness)
)
rib = (
    base.faces(">Z")
    .workplane()
    .center(leg_width/2, leg_width/2)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
combined = base.union(rib)
hole_positions = [
    (hole_offset, hole_offset),
    (hole_offset, hole_offset),
    (hole_offset, hole_offset),
    (hole_offset, hole_offset),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
