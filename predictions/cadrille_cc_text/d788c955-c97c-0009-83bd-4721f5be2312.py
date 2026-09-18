import cadquery as cq
height_vert = 40.0
thickness = 10.0
thickness = 12.0
length_horiz = 30.0
pocket_width = 20.0
pocket_depth = 6.0
hole_diameter = 8.0
fillet_radius = 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(length_horiz, 0)
    .lineTo(length_horiz, thickness)
    .lineTo(0, thickness)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").edges().chamfer(pocket_depth)
solid = solid.faces(">Z").edges().fillet(fillet_radius)
hole_positions = [
    (hole_diameter/2, hole_diameter/2),
    (hole_diameter/2, hole_diameter/2 + 5),
    (hole_diameter/2 + 5, hole_diameter/2 + 5),
]
solid = (
    solid.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .circle(hole_diameter/2)
    .cutBlind(-thickness)
)
solid = solid.edges().fillet(fillet_radius)
result = solid
