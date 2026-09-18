import cadquery as cq
outer_radius = 45
inner_radius = 30
height = 20
wall_thickness = 5
inner_radius = inner_radius - wall_thickness
chamfer_distance = 1
hole_diameter = 4
hole_spacing = 15
hole_count = 6
hole_count = 6
hole_radius = hole_diameter / 2
hole_radius = hole_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
result = solid
