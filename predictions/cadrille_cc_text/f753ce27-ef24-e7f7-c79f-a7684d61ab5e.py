import cadquery as cq
corner_radius = 20.0
wall_thickness = 5.0
height = 40.0
thick = 30.0
corner_radius = corner_radius - wall_thickness
pilot_hole_diameter = 4.0
chamfer_size = 1.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(corner_radius, 0)
    .lineTo(corner_radius, height)
    .lineTo(corner_radius + corner_radius, height)
    .lineTo(corner_radius + corner_radius, height)
    .lineTo(corner_radius + corner_radius, height)
    .lineTo(corner_radius, height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(pilot_hole_diameter)
solid = solid.faces(">Z").workplane().hole(pilot_hole_diameter)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
