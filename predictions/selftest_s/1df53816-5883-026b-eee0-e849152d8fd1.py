
import cadquery as cq

# Parameters
base_width = 80.0
base_height = 70.0
thickness = 10.0
fillet_radius = 2.0
chamfer_distance = 1.5
boss_diameter = 30.0
boss_height = 8.0
mount_hole_dia = 8.0
mount_hole_spacing = 60.0
rib_thickness = 3.0
rib_width = 20.0
rib_height = 15.0
slot_width = 15.0
slot_depth = 4.0

# Base triangular tab
result = (
    cq.Workplane("XY")
    .polyline([
        (-base_width/2, 0),
        (base_width/2, 0),
        (0, base_height)
    ])
    .close()
    .extrude(thickness)
)

# Fillet outer edges (skip base)
result = (
    result.edges()
    .filter(lambda e: e.geomType() == "LINE" and abs(e.Center().z) > 1e-6)
    .fillet(fillet_radius)
)

# Chamfer the base edge
result = (
    result.edges()
    .filter(lambda e: e.geomType() == "LINE" and abs(e.Center().z) < 1e-6)
    .chamfer(chamfer_distance)
)

# Central boss on top face (unioned)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .circle(boss_diameter/2)
    .extrude(boss_height)
)

# Mounting holes through full thickness on base line
for x_off in (-mount_hole_spacing/2, mount_hole_spacing/2):
    result = (
        result.faces("<Z").workplane()
        .center(x_off, 0)
        .hole(mount_hole_dia)
    )

# Rear rib for stiffness on -Y side (unioned)
result = (
    result.faces("<Y").workplane()
    .center(0, -rib_width/2)
    .rect(rib_thickness, rib_height)
    .extrude(thickness)
)

# Slot cut for pivot arm clearance across the top face
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .rect(slot_width, slot_depth)
    .cutBlind(-thickness/2)
)
