import cadquery as cq
block_length = 80.0
block_width = 40.0
block_height = 20.0
boss_radius = 12.0
boss_height = 10.0
boss_depth = 25.0
fillet_radius = 2.0
hole_diameter = 6.0
hole_depth = 25.0
hole_count = 6
hole_margin = 10.0
chamfer_distance = 1.0
rib_height = 8.0
rib_thickness = 4.0
rib_spacing = 10.0
base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_depth)
)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_depth)
)
combined = base.union(boss)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cskHole(hole_diameter, hole_depth, hole_count)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cskHole(hole_diameter, hole_depth, hole_count)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cskHole(hole_diameter, hole_depth, hole_count)
)
result = combined
