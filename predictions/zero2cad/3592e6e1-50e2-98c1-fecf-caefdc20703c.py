import cadquery as cq

rail_length = 100.0
rail_width = 30.0
rail_thickness = 8.0
rib_width = 12.0
rib_height = 3.0
hole_diameter = 2.0
hole_spacing = 18.0
hole_offset = 15.0
chamfer_size = 0.8
boss_diameter = 8.0
boss_height = 6.0
slot_width = 6.0
slot_length = 15.0
slot_depth = 4.0

base = cq.Workplane("XY").box(rail_length, rail_width, rail_thickness)

rib = (
    cq.Workplane("XY")
    .box(rail_length, rib_width, rib_height)
    .translate((0, 0, rail_thickness / 2 + rib_height / 2))
)

boss = (
    cq.Workplane("XY")
    .center(-rail_length / 2 + boss_diameter, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    .translate((0, 0, rail_thickness / 2 + rib_height - boss_height / 2))
)

slot = (
    cq.Workplane("XY")
    .center(rail_length / 2 - slot_depth / 2, 0)
    .rect(slot_length, slot_width)
    .extrude(slot_depth)
    .translate((0, 0, rail_thickness / 2 - slot_depth / 2))
)

combined = base.union(rib).union(boss).cut(slot)

num_holes = int((rail_length - 2 * hole_offset) / hole_spacing) + 1
hole_positions = [(-rail_length / 2 + hole_offset + i * hole_spacing, 0) for i in range(num_holes)]

result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)
