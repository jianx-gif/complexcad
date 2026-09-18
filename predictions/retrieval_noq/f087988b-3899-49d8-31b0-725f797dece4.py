
import cadquery as cq

outer_diameter = 80.0
wall_thickness = 4.0
ring_height = 12.0
boss_diameter = 30.0
boss_height = 10.0
central_hole_diameter = 6.0
counterbore_diameter = 10.0
counterbore_depth = 4.0
offset_hole_radius = 30.0
offset_hole_diameter = 5.0
slot_width = 8.0
slot_height = ring_height - 2 * wall_thickness
slot_depth = wall_thickness + 1.0
chamfer_size = 1.0

base_cylinder = cq.Workplane('XY').circle(outer_diameter / 2).extrude(ring_height)
thin_ring = base_cylinder.shell(-wall_thickness)
slot_cut = (
    thin_ring
    .faces('>Z')
    .workplane()
    .rect(slot_width, slot_height)
    .cutBlind(-slot_depth)
)
# Central boss
boss = cq.Workplane('XY', origin=(0, 0, ring_height)).circle(boss_diameter / 2).extrude(boss_height)
combined = slot_cut.union(boss)
# Counterbore through central boss using separate cylinders
central_hole = (
    cq.Workplane('XY', origin=(0, 0, ring_height + boss_height))
    .circle(central_hole_diameter / 2)
    .extrude(-boss_height)
)
central_counterbore = (
    cq.Workplane('XY', origin=(0, 0, ring_height + boss_height))
    .circle(counterbore_diameter / 2)
    .extrude(-counterbore_depth)
)
combined = combined.cut(central_hole).cut(central_counterbore)
# Offset counterbore holes through ring thickness
offset_points = [(offset_hole_radius, 0), (-offset_hole_radius, 0)]
through_holes = (
    cq.Workplane('XY', origin=(0, 0, ring_height))
    .pushPoints(offset_points)
    .circle(offset_hole_diameter / 2)
    .extrude(-ring_height)
)
through_counterbores = (
    cq.Workplane('XY', origin=(0, 0, ring_height))
    .pushPoints(offset_points)
    .circle(counterbore_diameter / 2)
    .extrude(-counterbore_depth)
)
combined = combined.cut(through_holes).cut(through_counterbores)
# Chamfers for safety
combined = (
    combined
    .edges('|Z')
    .chamfer(chamfer_size)
    .edges('>Z')
    .chamfer(chamfer_size)
)
result = combined
