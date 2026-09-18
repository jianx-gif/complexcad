import cadquery as cq

outer_dia = 60.0
total_height = 30.0
inner_dia = 30.0
wall_thickness = (outer_dia - inner_dia) / 2
chamfer_size = 1.5
slot_width = 12.0
slot_height = 8.0
slot_depth = 5.0
rib_thick = 2.0
rib_width = 6.0
rib_height = 12.0
mount_hole_dia = 5.0
mount_hole_offset = 15.0
num_mount_holes = 4

# Base outer cylinder
outer = cq.Workplane('XY').circle(outer_dia / 2).extrude(total_height)

# Central bore through full height
body = outer.faces('>Z').workplane().hole(inner_dia)

# Side slot for key (cut from side surface)
body = body.workplane().transformed(offset=(outer_dia / 2, 0, total_height / 2), rotate=(0, 90, 0)).rect(slot_width, slot_height).cutBlind(-slot_depth)

# Add internal ribs for strength (four equally spaced)
rib_base = cq.Workplane('XY').transformed(offset=(inner_dia / 2 + wall_thickness / 2, 0, total_height / 2 - rib_thick / 2)).rect(rib_width, rib_height).extrude(rib_thick)
for angle in [0, 90, 180, 270]:
    rib_rot = rib_base.rotate((0, 0, 0), (0, 0, 1), angle)
    body = body.union(rib_rot)

# Mounting holes on top face, arranged in square pattern
hole_points = [
    ( mount_hole_offset,  mount_hole_offset),
    (-mount_hole_offset,  mount_hole_offset),
    (-mount_hole_offset, -mount_hole_offset),
    ( mount_hole_offset, -mount_hole_offset)
]
body = body.faces('>Z').workplane().pushPoints(hole_points).hole(mount_hole_dia)

# Chamfer entry of bore and top outer edge for safety
result = body.edges('|Z').chamfer(chamfer_size)
