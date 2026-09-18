import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
rib_height = 12.0
rib_width = 6.0
rib_spacing = 15.0
rib_count = 4
chamfer_size = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, rib_height)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, rib_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces("<Z").workplane().hole(inner_radius * 2)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_width, depth=rib_height)
solid = solid.faces(">Z").workplane().center(0, 0).hole(rib_width, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_width, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_width, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_width, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_width, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_width, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_width, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_width, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_width, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_width, depth=rib_height)
result = solid
