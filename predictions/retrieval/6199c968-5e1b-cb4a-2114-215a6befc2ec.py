import cadquery as cq

# Parameters
plate_thickness = 5.0
sleeve_length = 60.0
outer_radius = 30.0
inner_radius = outer_radius - plate_thickness
flange_width = 8.0
flange_height = 10.0
slot_width = 6.0
slot_height = 30.0
inner_chamfer = 1.0

# Profile points for revolve (XZ plane)
profile_points = [
    (inner_radius, 0),
    (outer_radius, 0),
    (outer_radius, sleeve_length),
    (outer_radius + flange_width, sleeve_length),
    (outer_radius + flange_width, sleeve_length - flange_height),
    (outer_radius, sleeve_length - flange_height),
    (inner_radius, sleeve_length),
    (inner_radius, 0)
]

sleeve = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve()
)

slot_center_x = inner_radius + plate_thickness / 2
slot = (
    cq.Workplane("XY")
    .center(slot_center_x, 0)
    .box(slot_width, 30, slot_height, centered=True)
    .translate((0, 0, (sleeve_length - slot_height) / 2))
)

result = (
    sleeve
    .cut(slot)
    .faces("<X")
    .edges()
    .chamfer(inner_chamfer)
)
