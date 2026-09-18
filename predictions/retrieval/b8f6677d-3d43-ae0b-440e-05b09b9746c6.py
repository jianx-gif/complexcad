import cadquery as cq

# Parameters
body_length = 80.0
body_width = 40.0
body_thickness = 10.0
clamp_radius = 20.0
boss_width = 20.0
boss_depth = 25.0
boss_height = 12.0
hole_diameter = 5.0
chamfer_size = 2.0

# Base plate
base = cq.Workplane('XY').box(body_width, body_length, body_thickness, centered=(True, True, False))

# Revolved clamp jaw attached to right side of base
clamp_jaw = (
    cq.Workplane('YZ')
    .center(body_width / 2.0, 0)
    .moveTo(0, 0)
    .lineTo(0, clamp_radius)
    .threePointArc((clamp_radius / 2.0, clamp_radius * 1.2), (clamp_radius, clamp_radius))
    .lineTo(clamp_radius, 0)
    .close()
    .revolve(180, (0, 0, 0), (0, 1, 0))
)

# Rectangular boss on top of base
boss = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(boss_width, boss_depth)
    .extrude(boss_height)
    .translate((0, 0, body_thickness))
)

# Combine base, jaw, and boss
combined = base.union(clamp_jaw).union(boss)

# Clearance hole through boss (centered) using cylinder cut
hole = (
    cq.Workplane('XY')
    .center(0, 0)
    .circle(hole_diameter / 2.0)
    .extrude(body_thickness + boss_height)
)

# Chamfer wedge for boss front-top edge
wedge = (
    cq.Workplane('YZ')
    .moveTo(0, 0)
    .lineTo(chamfer_size, 0)
    .lineTo(0, chamfer_size)
    .close()
    .extrude(boss_width, both=True)
    .translate((0, boss_depth / 2.0, body_thickness + boss_height))
)

# Apply hole and chamfer wedge cuts
result = combined.cut(hole).cut(wedge)
