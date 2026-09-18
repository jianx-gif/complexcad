import cadquery as cq

# Parameters
outer_diameter = 80.0
wall_thickness = 2.0
channel_height = 40.0
screw_hole_diameter = 4.0
screw_hole_count = 8
screw_hole_radius = (outer_diameter/2) - wall_thickness/2
chamfer_distance = 0.5
base_plate_thickness = 5.0
base_plate_width = outer_diameter + 20.0
base_plate_length = outer_diameter + 20.0
pocket_width = 30.0
pocket_length = 20.0
pocket_depth = 5.0

# Create thin-walled cylindrical channel via revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter/2, 0)
    .lineTo(outer_diameter/2, channel_height)
    .lineTo((outer_diameter/2) - wall_thickness, channel_height)
    .lineTo((outer_diameter/2) - wall_thickness, 0)
    .close()
)

channel = profile.revolve()

# Add base plate at bottom
base_plate = (
    cq.Workplane("XY")
    .rect(base_plate_width, base_plate_length)
    .extrude(base_plate_thickness)
)

# Combine channel and base plate
combined = channel.union(base_plate)

# Add rectangular pocket on top surface
combined = (
    combined
    .faces(">Z")
    .workplane()
    .rect(pocket_width, pocket_length)
    .cutBlind(-pocket_depth)
)

# Drill screw holes around circumference at mid-height
combined = (
    combined
    .faces(">Z")
    .workplane(offset=channel_height/2)
    .polarArray(radius=screw_hole_radius, startAngle=0, angle=360, count=screw_hole_count)
    .hole(screw_hole_diameter)
)

# Apply chamfer to outer edges
result = combined.edges("|Z").chamfer(chamfer_distance)
