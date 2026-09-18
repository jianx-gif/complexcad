import cadquery as cq
outer_radius = 20.0
inner_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XY")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().rect(inner_radius, inner_radius).cutBlind(-inner_radius)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_radius, startAngle=0, count=hole_count, angle=360).hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count).hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count).hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=inner_radius, startAngle=0, angle=360, count=hole_count).hole(hole_diameter)
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
