import cadquery as cq
outer_radius = 30.0
outer_height = 25.0
shaft_radius = 8.0
shaft_height = 10.0
insert_radius = 3.0
insert_length = 12.0
insert_height = 10.0
insert_radius = 3.0
dome_height = 8.0
dome_radius = 25.0
dome_height = 8.0
chamfer_size = 1.0
grip_ring_thickness = 2.0
grip_ring_depth = 4.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(shaft_radius, 0)
    .lineTo(shaft_radius, shaft_height)
    .lineTo(shaft_radius + insert_radius, shaft_height)
    .lineTo(shaft_radius + insert_radius, shaft_height + insert_height)
    .lineTo(0, shaft_height + insert_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(insert_radius * 2)
solid = solid.faces(">Z").workplane().hole(insert_radius * 2)
solid = solid.faces(">Z").workplane().polarArray(radius=insert_radius, count=insert_radius, startAngle=0, angle=360).hole(central_hole_radius * 2)
solid = solid.faces(">Z").workplane().polarArray(radius=insert_radius - groove_ring_thickness/2, count=insert_radius/2, startAngle=0, angle=360).circle(grip_ring_thickness).cutBlind(-grip_ring_depth)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_ring_radius, count=insert_radius/2, startAngle=0, angle=360).circle(grip_ring_thickness).cutBlind(-grip_ring_depth)
result = solid
