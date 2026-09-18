import cadquery as cq

# Parameters
outer_radius = 30.0
wall_thickness = 3.0
inner_radius = outer_radius - wall_thickness
height = 60.0
taper_height = 10.0
taper_delta = 5.0
top_section_height = 10.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_z = 30.0

# Outer profile sketch on XZ plane
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height - taper_height - top_section_height)
    .lineTo(outer_radius - taper_delta, height - top_section_height)
    .lineTo(outer_radius - taper_delta, height)
    .lineTo(0, height)
    .close()
)

# Inner profile sketch (offset inward)
inner_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(inner_radius, 0)
    .lineTo(inner_radius, height - taper_height - top_section_height)
    .lineTo(inner_radius - taper_delta, height - top_section_height)
    .lineTo(inner_radius - taper_delta, height)
    .lineTo(0, height)
    .close()
)

# Revolve profiles to create solids
outer_solid = outer_profile.revolve()
inner_solid = inner_profile.revolve()

# Hollow shell by subtraction
hollow_shell = outer_solid.cut(inner_solid)

# Chamfer top rim edges
chamfered = hollow_shell.faces(">Z").edges().chamfer(chamfer_distance)

# Add mounting holes on top face
result = (
    chamfered
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, hole_offset_z), (hole_spacing/2, hole_offset_z)])
    .hole(hole_diameter)
)
