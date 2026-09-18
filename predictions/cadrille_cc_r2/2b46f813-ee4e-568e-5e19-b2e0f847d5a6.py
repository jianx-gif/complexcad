import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 15.0
hole_offset = 10.0
profile = (
    cq.Workplane('XZ')
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, outer_radius)
    .lineTo(outer_radius, outer_radius)
    .lineTo(outer_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces('>Z').workplane().hole(hole_diameter)
solid = solid.faces('>Z').workplane().hole(hole_diameter)
solid = solid.faces('>Z').edges().chamfer(chamfer_distance)
result = solid
