import cadquery as cq
block_width = 60.0
block_depth = 20.0
block_height = 15.0
arc_radius = 50.0
boss_radius = 8.0
boss_height = 5.0
top_fillet = 1.0
rib_thickness = 2.0
rib_width = 5.0
rib_height = 3.0
rib_offset = 10.0
chamfer = 0.5
base = (
    cq.Workplane("XY")
    .circle(block_width / 2)
    .extrude(block_depth)
)
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
)
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
)
result = base.union(boss)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_thickness, rib_width)
    .extrude(rib_height)
)
result = result.edges("|Z").fillet(top_fillet)
result = result.edges("|Z").chamfer(chamfer)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(tap_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_height)
)
