import cadquery as cq
leg_length = 80.0
leg_width = 30.0
wall_thickness = 2.0
inner_radius = 15.0
inner_radius = inner_radius + wall_thickness
rib_height = 10.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_length, 0),
        (leg_length, leg_width),
        (leg_width, leg_width),
        (leg_width, leg_length),
        (0, leg_length),
    ])
    .close()
    .extrude(leg_length)
)
rib = (
    base.faces(">Z")
    .workplane()
    .center(leg_width/2, leg_width/2)
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
rib = (
    rib.faces(">Z")
    .workplane()
    .center(leg_width/2, leg_width/2)
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
combined = base.union(rib)
result = combined.edges("|Z").chamfer(chamfer_size)
