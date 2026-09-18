import cadquery as cq
outer_radius = 45.0
inner_radius = 25.0
thickness = 15.0
profile = (
    cq.Workplane('XZ')
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, thickness/2)
    .lineTo(outer_radius, thickness/2)
    .lineTo(outer_radius, thickness)
    .lineTo(inner_radius, thickness)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(1.0)
result = solid.split(cq.Plane.YZ)
