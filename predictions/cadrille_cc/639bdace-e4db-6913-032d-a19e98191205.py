import cadquery as cq
outer_radius = 30
wall_thickness = 5
inner_radius = outer_radius - wall_thickness
base_thickness = 8
rib_width = 10
rib_height = 12
rib_thickness = 4
rib_spacing = 12
chamfer_size = 1
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, base_thickness)
    .lineTo(outer_radius, base_thickness + rib_height)
    .lineTo(outer_radius, base_thickness + rib_height)
    .lineTo(inner_radius, base_thickness)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, rib_thickness)
    .translate((outer_radius - rib_thickness/2, 0, rib_thickness/2))
)
solid = solid.union(rib)
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().center(0, 0).hole(rib_thickness)
solid = solid.faces(">Z").workplane().center(0, 0).hole(rib_thickness, depth=rib_height)
solid = solid.faces(">Z").workplane().center(0, 0).hole(rib_thickness, depth=rib_height)
solid = solid.faces(">Z").workplane().center(0, 0).hole(rib_thickness, depth=rib_height)
solid = solid.faces(">Z").workplane().center(0, 0).hole(rib_thickness, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_thickness, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_thickness, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_thickness, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_thickness, depth=rib_height)
solid = solid.faces("<Z").workplane().center(0, 0).hole(rib_thickness, depth=rib_height)
result = solid
