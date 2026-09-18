import cadquery as cq
height = 80.0
wall_thickness = 2.0
inner_radius = radius_bottom - wall_thickness
inner_radius = radius_top - wall_thickness
inner_radius = radius_top - wall_thickness
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius + wall_thickness
inner_radius = inner_radius + wall_thickness
inner_radius = inner_radius + wall_thickness
chamfer_size = 0.8
profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius + wall_thickness, height)
    .lineTo(inner_radius + wall_thickness, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
