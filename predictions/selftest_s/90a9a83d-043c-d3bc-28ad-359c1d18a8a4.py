import cadquery as cq

# Parameters
outer_diameter = 80.0
inner_diameter = 30.0
spacer_height = 12.0
central_hole_diameter = 15.0
rib_thickness = 5.0
rib_width = 6.0
mounting_hole_diameter = 5.0
mounting_hole_offset = 5.0
chamfer_distance = 1.0

# Derived values
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
rib_outer_radius = inner_radius + rib_thickness
rib_start_z = (spacer_height - rib_width) / 2.0

# Build the revolved profile on the XZ plane
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, spacer_height)
    .lineTo(inner_radius, spacer_height)
    .lineTo(inner_radius, rib_start_z + rib_width)
    .lineTo(rib_outer_radius, rib_start_z + rib_width)
    .lineTo(rib_outer_radius, rib_start_z)
    .lineTo(inner_radius, rib_start_z)
    .lineTo(inner_radius, 0)
    .close()
)

# Revolve the profile around the Z axis to create the spacer ring with internal rib
spacer = profile.revolve()

# Cut central through‑hole
spacer = spacer.faces(">Z").workplane().hole(central_hole_diameter)

# Add four equally spaced mounting holes on the outer face
mounting_radius = outer_radius - mounting_hole_offset
spacer = (
    spacer.faces(">Z")
    .workplane()
    .pushPoints([
        (mounting_radius, 0),
        (0, mounting_radius),
        (-mounting_radius, 0),
        (0, -mounting_radius),
    ])
    .hole(mounting_hole_diameter)
)

# Apply chamfer to the outer top rim edges for safety
spacer = spacer.faces(">Z").edges().chamfer(chamfer_distance)

result = spacer
