import cadquery as cq

# Parameters
arm_length = 80.0
base_radius = 12.0
rib_start = 45.0
rib_end = 55.0
rib_thickness = 4.0
rib_outer_radius = base_radius + rib_thickness
rib_outer_radius_end = rib_outer_radius + 5.0
hole_diameter = 5.0
hole_depth = 12.0
hole_offset = base_radius - 2.0
chamfer_size = 0.5

# Base profile for revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, rib_start)
    .lineTo(rib_outer_radius, rib_start)
    .lineTo(rib_outer_radius_end, rib_end)
    .lineTo(base_radius, rib_end)
    .lineTo(base_radius, arm_length)
    .lineTo(0, arm_length)
    .close()
)

# Revolve to create solid
solid = profile.revolve()

# Add blind holes on the base face
result = (
    solid
    .faces("<Y")
    .workplane()
    .pushPoints([(-hole_offset, 0), (hole_offset, 0)])
    .hole(hole_diameter, depth=hole_depth)
    .edges("|Y")
    .chamfer(chamfer_size)
)
