import cadquery as cq
outer_diameter = 80.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = outer_diameter / 2.0
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().center(0, 0).circle(inner_radius).cutBlind(-wall_thickness)
solid = solid.faces(">Z").workplane().center(0, 0).circle(inner_radius).cutBlind(-wall_thickness)
solid = solid.faces(">Z").workplane().center(0, 0).circle(inner_radius).cutBlind(-wall_thickness)
solid = solid.faces(">Z").workplane().center(0, 0).circle(inner_radius).cutBlind(-wall_thickness)
solid = solid.faces(">Z").workplane().center(0, 0).circle(inner_radius).cutBlind(-wall_thickness)
solid = solid.faces(">Z").workplane().center(0, 0).circle(inner_radius).cutBlind(-wall_thickness)
solid = solid.faces(">Z").workplane().center(0, 0).circle(inner_radius).cutBlind(-wall_thickness)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
