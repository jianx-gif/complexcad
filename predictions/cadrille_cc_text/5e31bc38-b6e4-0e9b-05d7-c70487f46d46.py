import cadquery as cq
corner_radius = 30.0
pipe_radius = 10.0
pipe_radius = pipe_radius + pipe_radius
boss_radius = 8.0
boss_height = 20.0
hole_diameter = 6.0
hole_spacing = 30.0
boss_fillet = 4.0
boss_radius = 8.0
boss_fillet = boss_radius
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(corner_radius, 0)
    .lineTo(corner_radius, corner_radius)
    .lineTo(corner_radius, corner_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(boss_radius)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_spacing, startAngle=0, angle=360, count=hole_spacing).hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_spacing, startAngle=0, angle=360, count=hole_spacing).hole(hole_diameter)
result = solid
