import cadquery as cq
base_height = 10.0
base_radius = 8.0
cam_radius = 15.0
hub_radius = 5.0
hub_height = 12.0
slot_width = 8.0
slot_height = 4.0
chamfer = 0.8
slot_depth = 5.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, base_height)
    .lineTo(0, base_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer)
solid = solid.faces(">Z").workplane().hole(hub_radius * 2)
solid = solid.faces(">Z").workplane().hole(hub_radius * 2)
solid = solid.faces(">Z").workplane().rect(slot_width, slot_height).cutBlind(-slot_depth)
solid = solid.faces(">Z").workplane().center(0, 0).rect(slot_width, slot_height).cutBlind(-slot_depth)
result = solid
