import cadquery as cq

outer_radius = 45.0
inner_radius = 30.0
height = 30.0
wall_thickness = 5.0
fillet_radius = 2.0
latch_width = 12.0
latch_thickness = 3.0
latch_height = 12.0
latch_offset = 5.0

profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius - wall_thickness, height)
    .threePointArc((inner_radius + wall_thickness, height/2), (inner_radius, 0))
    .close()
)

shell = profile.revolve()

shell = shell.faces(">Z").edges().fillet(fillet_radius)

latch = (
    cq.Workplane("XY")
    .box(latch_thickness, latch_width, latch_height)
    .translate((outer_radius - latch_thickness/2, 0, height - latch_offset - latch_height/2))
)

result = shell.union(latch)
