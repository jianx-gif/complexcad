import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
height = 70.0
entry_chamfer = 2.0
hole_circle_radius = 15.0
hole_count = 8
hole_depth = 2.0
notch_width = 8.0
notch_height = 12.0
notch_depth = 2.0
outer_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(entry_chamfer)
solid = solid.faces(">Z").workplane().hole(clear_hole_diameter)
solid = solid.faces(">Z").edges().chamfer(entry_chamfer)
hole_positions = [
    (hole_circle_radius * math.cos(math.radians(a)), hole_circle_radius * math.sin(math.radians(a)))
    for a in range(hole_count)
]
solid = (
    solid.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(clear_hole_diameter)
)
solid = solid.edges().chamfer(entry_chamfer)
result = solid
