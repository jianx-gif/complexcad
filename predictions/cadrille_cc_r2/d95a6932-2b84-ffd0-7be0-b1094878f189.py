import cadquery as cq
outer_radius = 45
inner_radius = 30
height = 80
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
base_thickness = 5
inner_radius = inner_radius - wall_thickness
base_height = height - 20
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(outer_radius)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().rect(inner_radius, inner_radius).cutBlind(-wall_thickness)
solid = solid.faces(">Z").workplane().rect(inner_radius, inner_radius).cutBlind(-wall_thickness)
solid = solid.faces(">Z").workplane().rect(inner_radius, inner_radius).cutBlind(-wall_thickness).cutBlind(-wall_thickness)
solid = solid.faces(">Z").workplane().rect(inner_radius, inner_radius).cutBlind(-wall_thickness).cutBlind(-wall_thickness)
solid = solid.faces(">Z").workplane().rect(inner_radius, inner_radius).cutBlind(-wall_thickness).cutBlind(-wall_thickness)
result = solid
