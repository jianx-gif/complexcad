import cadquery as cq
plate_length = 80.0
plate_width = 80.0
plate_thickness = 5.0
boss_base_radius = 12.0
boss_height = 12.0
corner_hole_diameter = 5.0
corner_hole_offset = 10.0
edge_chamfer = 1.0
slot_length = 30.0
slot_width = 6.0
slot_offset_from_center = 20.0
base_plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .moveTo(boss_base_radius, 0)
    .lineTo(boss_base_radius, boss_height)
    .lineTo(boss_top_radius, boss_height)
    .lineTo(0, boss_height)
    .close()
    .revolve()
)
base_plate = base_plate.union(boss)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(slot_length, slot_width)
    .extrude(plate_thickness)
    .translate((0, 0, plate_thickness))
)
base_plate = base_plate.union(boss)
boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(slot_length, slot_width)
    .extrude(plate_thickness)
)
boss = boss.cut(boss)
boss = boss.edges("|Z").chamfer(edge_chamfer)
result = base_plate.union(boss)
