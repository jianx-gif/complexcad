import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 10.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
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
    (0, hole_offset),
]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined.edges("|Z").fillet(fillet_radius)
