import cadquery as cq
outer_radius = 40.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = inner_radius - wall_thickness
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_count = 3
hole_count = 3
hole_offset = outer_radius - wall_thickness/2
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
