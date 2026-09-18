import cadquery as cq
outer_radius = 30.0
inner_radius = 10.0
outer_height = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius + wall_thickness
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 4
hole_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, outer_height - wall_thickness)
    .lineTo(inner_radius, outer_height - wall_thickness)
    .lineTo(inner_radius, outer_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter)
)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, count=hole_count, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter)
)
result = solid
