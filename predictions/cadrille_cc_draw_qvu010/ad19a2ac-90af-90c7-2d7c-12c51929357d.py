import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 12
hole_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius, inner_radius + wall_thickness)
    .lineTo(inner_radius + wall_thickness, inner_radius + wall_thickness)
    .lineTo(inner_radius, inner_radius + wall_thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, count=hole_count, startAngle=0, angle=360)
    .hole(hole_diameter)
)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter)
)
result = solid
