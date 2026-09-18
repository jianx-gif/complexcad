import cadquery as cq
outer_radius = 20.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius + wall_thickness
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_offset = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, inner_radius)
    .lineTo(inner_radius, inner_radius)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = (
    solid.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(inner_radius * 2, inner_radius * 2)
    .cutBlind(-chamfer_size)
)
solid = (
    solid.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(hole_spacing, hole_spacing)
    .cutBlind(-hole_offset)
)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
