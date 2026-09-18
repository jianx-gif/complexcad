import cadquery as cq

plate_length = 80
plate_width = 60
plate_thickness = 5
corner_fillet_radius = 5
mount_hole_diameter = 6
mount_hole_spacing = 40
rib_height = 4
rib_thickness = 5
rib_spacing = 20
insert_diameter = 8
insert_depth = 5  # countersink depth equal to thickness
insert_thread_diameter = 6
insert_thread_length = 8
chamfer_distance = 0.8

# Base plate
base_plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
base_plate = base_plate.edges("(>X and >Y and |Z)").fillet(corner_fillet_radius)

# Central recessed pocket (half thickness deep)
recess_depth = plate_thickness / 2
pocket = (
    base_plate.faces("+Z").workplane()
    .rect(plate_length * 0.6, plate_width * 0.4)
    .extrude(-recess_depth)
)
base_plate = base_plate.cut(pocket)

# Add ribs on top surface
rib_count = int((plate_width - rib_spacing) // (rib_spacing + rib_thickness))
for i in range(rib_count):
    y_offset = -plate_width/2 + rib_spacing + i*(rib_spacing + rib_thickness) + rib_thickness/2
    rib = (
        base_plate.faces("+Z").workplane()
        .center(0, y_offset)
        .rect(plate_length * 0.8, rib_thickness)
        .extrude(rib_height)
    )
    base_plate = base_plate.union(rib)

# Mounting holes (symmetrical)
for x in [-mount_hole_spacing/2, mount_hole_spacing/2]:
    base_plate = base_plate.faces("-Z").workplane().center(x, 0).hole(mount_hole_diameter)

# Threaded insert cavities (countersink + blind hole)
for x in [-mount_hole_spacing/2, mount_hole_spacing/2]:
    base_plate = base_plate.faces("-Z").workplane().center(x, 0).cskHole(insert_diameter, insert_diameter/2, insert_depth)
    base_plate = base_plate.faces("-Z").workplane().center(x, 0).hole(insert_thread_diameter, insert_thread_length)

# Chamfer outer edges for safety
result = base_plate.edges("|Z").chamfer(chamfer_distance)
