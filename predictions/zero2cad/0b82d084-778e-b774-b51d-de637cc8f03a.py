import cadquery as cq

# Parameters
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 2.0
flange_width = 10.0
flange_thickness = 5.0
channel_height = 20.0
fillet_radius = 0.5
hole_diameter = 5.0
hole_count = 2
rib_thickness = 2.0
rib_height = 8.0
rib_offset = 5.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius + flange_width, 0)
    .lineTo(outer_radius + flange_width, flange_thickness)
    .lineTo(outer_radius, flange_thickness)
    .lineTo(outer_radius, channel_height)
    .threePointArc((inner_radius + wall_thickness, channel_height - wall_thickness), (inner_radius, channel_height - wall_thickness))
    .lineTo(inner_radius, 0)
    .close()
)

# Revolve to create thin-walled channel with flange
result = profile.revolve()

# Fillet inner bottom edge for safety
result = result.edges("<Z and <X").fillet(fillet_radius)

# Add mounting holes on flange (circular pattern)
hole_radius = outer_radius + flange_width/2
result = (
    result.faces("<Z")
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, count=hole_count, angle=180)
    .hole(hole_diameter)
)

# Add internal rib for stiffness (rectangular block attached to inner wall)
rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_thickness, rib_height)
    .translate((inner_radius - rib_thickness/2, 0, rib_offset + rib_height/2))
)
result = result.union(rib)

# Add a small pocket on outer flange for cable routing
pocket = (
    cq.Workplane("XY")
    .rect(flange_width/2, flange_thickness/2)
    .extrude(flange_thickness)
    .translate((outer_radius + flange_width/4, 0, flange_thickness/2))
)
result = result.cut(pocket)
