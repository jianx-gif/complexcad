import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
edge_chamfer = 0.8
central_hole_diameter = 12.0
mount_hole_diameter = 6.0
mount_hole_counterbore_diameter = 10.0
mount_hole_counterbore_depth = 2.0
mount_hole_offset = 6.0
rib_width = 8.0
rib_height = 3.0
rib_spacing = 20.0
blind_hole_diameter = 5.0
blind_hole_depth = 3.0
blind_hole_rows = 2
blind_hole_cols = 5
blind_hole_spacing_x = 15.0
blind_hole_spacing_y = 30.0
blind_hole_margin_x = 10.0
blind_hole_margin_y = 12.0

# Base plate
result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .edges()
    .chamfer(edge_chamfer)
)

# Central through hole
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(central_hole_diameter)
)

# Mounting holes with countersink at four corners
mount_points = [
    (-plate_length/2 + mount_hole_offset, -plate_width/2 + mount_hole_offset),
    ( plate_length/2 - mount_hole_offset, -plate_width/2 + mount_hole_offset),
    ( plate_length/2 - mount_hole_offset,  plate_width/2 - mount_hole_offset),
    (-plate_length/2 + mount_hole_offset,  plate_width/2 - mount_hole_offset),
]
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(mount_points)
    .cskHole(mount_hole_diameter, mount_hole_counterbore_diameter, mount_hole_counterbore_depth)
)

# Stiffening ribs on top surface (unioned to keep single solid)
rib_count = int((plate_length - 2*mount_hole_offset) // rib_spacing) + 1
rib_positions = [ -plate_length/2 + mount_hole_offset + i*rib_spacing for i in range(rib_count) ]
for x in rib_positions:
    rib = (
        cq.Workplane("XY")
        .center(x, 0)
        .rect(rib_width, plate_width - 2*mount_hole_offset)
        .extrude(rib_height)
    )
    result = result.union(rib)

# Blind holes pattern on bottom face
start_x = -plate_length/2 + blind_hole_margin_x
start_y = -plate_width/2 + blind_hole_margin_y
blind_points = []
for i in range(blind_hole_cols):
    for j in range(blind_hole_rows):
        x = start_x + i*blind_hole_spacing_x
        y = start_y + j*blind_hole_spacing_y
        blind_points.append((x, y))
result = (
    result
    .faces("<Z")
    .workplane()
    .pushPoints(blind_points)
    .hole(blind_hole_diameter, blind_hole_depth)
)
