import cadquery as cq
leg_length_long = 80.0
leg_length_short = 60.0
leg_thickness = 8.0
boss_radius = 10.0
boss_height = 30.0
boss_radius = boss_radius
boss_height = leg_thickness
countersink_diameter = 6.0
countersink_top_diameter = 12.0
countersink_angle = 82.0
countersink_depth = boss_height
chamfer_distance = 1.0
rib_thickness = 4.0
rib_spacing = 20.0
gusset_thickness = 5.0
gusset_height = leg_thickness + boss_height
gusset_angle = leg_thickness + boss_height
gusset_length = leg_length_short - 2 * boss_radius
gusset_offset = leg_length_short / 2
base = (
    cq.Workplane("XY")
    .box(leg_length_long, leg_thickness, leg_thickness)
    .translate((leg_length_long/2 - leg_thickness/2, 0, 0))
)
base = base.edges("|Z").chamfer(chamfer_distance)
boss = (
    cq.Workplane("XY")
    .box(boss_radius, boss_radius, boss_height)
    .translate((leg_length_long/2 - boss_radius, 0, 0))
)
base = base.union(boss)
gusset = (
    cq.Workplane("XY")
    .box(gusset_length, gusset_offset, gusset_thickness)
    .translate((leg_length_long/2 - gusset_offset, 0, 0))
)
base = base.union(gusset)
base = base.faces(">Z").edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_thickness, rib_thickness)
    .translate((leg_length_long/2 - gusset_offset, 0, 0))
)
result = base.union(rib)
