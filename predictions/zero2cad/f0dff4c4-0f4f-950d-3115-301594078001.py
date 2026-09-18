import cadquery as cq

outer_diameter = 80.0
inner_diameter = 30.0
collar_width = 20.0
groove_width = 5.0
groove_depth = 3.0
chamfer_size = 1.0
slot_width = 8.0
slot_length = 12.0
slot_depth = 10.0
boss_diameter = 35.0
boss_height = 4.0

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
groove_radius = outer_radius - groove_width

profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, collar_width)
    .lineTo(groove_radius, collar_width)
    .lineTo(groove_radius, collar_width - groove_depth)
    .lineTo(inner_radius, collar_width - groove_depth)
    .lineTo(inner_radius, 0)
    .close()
)

base = profile.revolve()

base = base.edges().chamfer(chamfer_size)

boss = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
    .translate((0, 0, collar_width - boss_height))
)

result = base.union(boss)

slot = (
    cq.Workplane("XY")
    .box(slot_length, slot_depth, collar_width)
    .translate((outer_radius - slot_length / 2.0, 0, collar_width / 2.0))
)

result = result.cut(slot)
