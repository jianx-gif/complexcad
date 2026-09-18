import cadquery as cq
outer_radius = 30.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 12
hole_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, inner_radius)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = (
    solid.faces(">Z").workplane()
    .polarArray(radius=hole_radius, startAngle=0, count=hole_count, angle=360)
    .hole(hole_diameter)
)
solid = (
    solid.faces(">Z").workplane()
    .polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter)
)
result = solid
