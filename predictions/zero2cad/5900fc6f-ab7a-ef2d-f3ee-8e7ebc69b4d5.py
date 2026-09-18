import cadquery as cq

# Parameters
arm_length = 80.0
tri_base = 30.0
tri_height = 20.0
boss_radius = 8.0
boss_length = 20.0
chamfer_dist = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
slot_width = 6.0
slot_length = 30.0
slot_offset = 15.0

# Triangular profile on YZ plane
tri_profile = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (tri_base, 0),
        (tri_base / 2, tri_height),
        (0, 0),
    ])
    .close()
)

# Straight sweep path along X axis
path = (
    cq.Workplane("XY")
    .lineTo(arm_length, 0)
    .wire()
)

# Sweep to create lever arm
lever = tri_profile.sweep(path, multisection=False)

# Chamfer tip edges (edges of the far X face)
lever = lever.faces(">X").edges().chamfer(chamfer_dist)

# Central cylindrical boss aligned with X axis
boss = (
    cq.Workplane("YZ")
    .center(tri_base / 2, 0)
    .circle(boss_radius)
    .extrude(boss_length)
)
lever = lever.union(boss)

# Mounting holes on the base face (near X=0)
lever = (
    lever.faces("<X")
    .workplane()
    .pushPoints([(-hole_offset, 0), (hole_offset, 0)])
    .hole(hole_diameter)
)

# Slot cut on the side face (positive Y direction)
lever = (
    lever.faces(">Y")
    .workplane()
    .center(slot_offset, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-tri_height)
)

result = lever