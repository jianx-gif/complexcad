import cadquery as cq

# Parameters
plate_width = 80.0
plate_depth = 50.0
plate_thickness = 10.0
wall_thickness = 5.0
rib_width = 8.0
rib_height = 12.0
rib_extra = 3.0
rib_spacing = 20.0
mount_hole_dia = 5.0
mount_hole_spacing = 40.0
fillet_radius = 1.0
chamfer_distance = 1.0
tab_length = 15.0
tab_height = 8.0
tab_thickness = wall_thickness
hook_depth = 2.0
hook_width = 4.0

# Base plate
base = cq.Workplane("XY").rect(plate_width, plate_depth).extrude(plate_thickness)

# Ribs on underside (bottom face)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_extra)
)
rib_positions = [
    (-plate_width/2 + rib_spacing, 0),
    (0, 0),
    (plate_width/2 - rib_spacing, 0),
]
for x, y in rib_positions:
    base = base.union(rib.translate((x, y, -rib_extra)))

# Mounting holes on top face (four corners of a square)
hole_positions = [
    (-mount_hole_spacing/2, -mount_hole_spacing/2),
    (mount_hole_spacing/2, -mount_hole_spacing/2),
    (mount_hole_spacing/2, mount_hole_spacing/2),
    (-mount_hole_spacing/2, mount_hole_spacing/2),
]
top_wp = base.faces(">Z").workplane()
for hx, hy in hole_positions:
    top_wp = top_wp.pushPoints([(hx, hy)])
base = top_wp.hole(mount_hole_dia)

# Fillet on outer edges of top face
base = base.faces(">Z").edges().fillet(fillet_radius)

# Chamfer on bottom edges for safety
base = base.faces("<Z").edges().chamfer(chamfer_distance)

# Snap‑fit tab on front face (+Y)
# Tab solid
tab = base.faces(">Y").workplane().rect(tab_thickness, tab_height).extrude(tab_length)
# Hook cut for snap‑fit
hook = (
    cq.Workplane("XY")
    .rect(hook_depth, hook_width)
    .extrude(tab_thickness + 0.2)
)
hook_z = plate_thickness/2 - hook_width/2
hook = hook.translate((0, plate_depth/2 + tab_length - hook_depth/2, hook_z))
# Combine
base = base.union(tab).cut(hook)

result = base