import cadquery as cq

# Parameters
plate_width = 80.0
plate_height = 80.0
plate_thickness = 5.0
central_hole_diameter = 15.0
rib_outer_diameter = 25.0
rib_inner_diameter = 20.0
rib_height = 2.0
fillet_radius = 1.5
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
slot_width = 6.0
slot_length = 30.0
slot_offset = 20.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)

# Central through hole
base = base.faces(">Z").workplane().hole(central_hole_diameter)

# Annular rib (raised ring) on top surface
rib = (
    cq.Workplane("XY")
    .circle(rib_outer_diameter / 2)
    .circle(rib_inner_diameter / 2)
    .extrude(rib_height)
)
base = base.union(rib)

# Fillet on rib outer vertical edge
base = base.edges("|Z and >X and >Y").fillet(fillet_radius)

# Mounting holes at four corners
mount_points = [
    (mount_hole_offset, mount_hole_offset),
    (-mount_hole_offset, mount_hole_offset),
    (-mount_hole_offset, -mount_hole_offset),
    (mount_hole_offset, -mount_hole_offset),
]
base = base.faces(">Z").workplane().pushPoints(mount_points).hole(mount_hole_diameter)

# Cable slot on one side
base = (
    base.faces(">Z")
    .workplane()
    .center(0, plate_height / 2 - slot_offset)
    .rect(slot_length, slot_width)
    .cutBlind(-plate_thickness)
)

result = base