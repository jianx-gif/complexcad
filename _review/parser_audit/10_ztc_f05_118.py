import cadquery as cq

# Parameter definitions
block_length = 80.0
block_width = 50.0
block_thickness = 15.0
corner_radius = 5.0
boss_radius = 12.0
boss_depth = 8.0
set_screw_hole_diameter = 4.0
threaded_hole_diameter = 6.0
hole_offset_x = 20.0
hole_offset_y = 15.0
counterbore_diameter = 8.0
counterbore_depth = 2.0
chamfer_distance = 0.5
pocket_length = 30.0
pocket_width = 20.0
pocket_depth = 4.0
rib_width = 4.0
rib_height = 5.0
rib_spacing = 20.0

# Base block
base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_thickness)
    .edges("|Z").chamfer(chamfer_distance)
)

# Central through slot (rectangular)
slot = (
    cq.Workplane("XY")
    .rect(30, 10)
    .extrude(block_thickness)
)
base = base.cut(slot)

# Recessed boss created by revolve and subtracted
boss = (
    cq.Workplane("XZ")
    .moveTo(boss_radius, 0)
    .lineTo(boss_radius, -boss_depth)
    .lineTo(0, -boss_depth)
    .close()
    .revolve()
    .translate((0, 0, block_thickness - boss_depth))
)
base = base.cut(boss)

# Counterbore on top surface
base = base.faces(">Z").workplane().hole(counterbore_diameter, depth=counterbore_depth)
# Through set screw hole (smaller) through full thickness
base = base.faces(">Z").workplane().hole(threaded_hole_diameter)

# Pocket on top face
base = base.faces(">Z").workplane().rect(pocket_length, pocket_width).cutBlind(pocket_depth)

# Reinforcement ribs on bottom face
bottom_wp = base.faces("<Z").workplane()
for x in (-rib_spacing/2, rib_spacing/2):
    rib = bottom_wp.center(x, 0).rect(rib_width, block_width).extrude(rib_height)
    base = base.union(rib)

result = base
