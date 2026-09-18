import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
base_radius = outer_radius - wall_thickness
base_height = 80.0
wall_thickness = 2.0
chamfer_distance = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, base_height)
    .lineTo(outer_radius, base_height + outer_radius)
    .lineTo(outer_radius, base_height + outer_radius)
    .lineTo(outer_radius, base_height + outer_radius)
    .lineTo(0, base_height + outer_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces("<Z").workplane().hole(inner_radius * 2)
solid = solid.faces("<Z").workplane().hole(inner_radius * 2)
solid = solid.faces("<Z").workplane().hole(inner_radius * 2)
solid = solid.faces("<Z").workplane().hole(inner_radius * 2)
solid = solid.faces("<Z").workplane().hole(inner_radius * 2)
solid = solid.faces("<Z").workplane().hole(inner_radius * 2)
solid = solid.faces("<Z").workplane().hole(inner_radius * 2)
result = solid
