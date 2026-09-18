import cadquery as cq

# Parameters
outer_radius = 30.0
inner_radius = 20.0
spacer_height = 50.0
shoulder_height = 8.0
central_hole_diameter = 12.0
countersink_hole_diameter = 6.0
countersink_diameter = 10.0
countersink_angle = 82.0
countersink_depth = 5.0
countersink_offset = 15.0
chamfer_size = 0.8

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, spacer_height - shoulder_height)
    .lineTo(inner_radius, spacer_height - shoulder_height)
    .lineTo(inner_radius, spacer_height)
    .lineTo(0, spacer_height)
    .close()
)

# Revolve to create Z spacer
spacer = profile.revolve()

# Central through hole
spacer = spacer.faces("<Z").workplane().hole(central_hole_diameter)

# Countersunk holes on top face
spacer = (
    spacer.faces("<Z")
    .workplane()
    .pushPoints([(-countersink_offset, 0), (countersink_offset, 0)])
    .cskHole(countersink_hole_diameter, countersink_diameter, countersink_angle, countersink_depth)
)

# Chamfer bottom outer edge
spacer = spacer.faces("<Z").edges().chamfer(chamfer_size)

result = spacer