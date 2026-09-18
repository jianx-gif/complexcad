import cadquery as cq

outer_diameter = 80
inner_diameter = 50
inner_radius = inner_diameter / 2
ring_thickness = 8
boss_height = 30
boss_base_radius = inner_radius - 5
extension_radius = inner_radius + 1
extension_height = 2
taper_height = 5
taper_width = 8
top_radius = boss_base_radius - taper_width
clearance_hole_diameter = 8
hole_count = 8
hole_pattern_radius = (boss_base_radius + top_radius) / 2
rib_width = 4
rib_height = 5
rib_length = (outer_diameter - inner_diameter) / 2 - 5
rib_center_radius = (inner_radius + outer_diameter / 2) / 2
chamfer_size = 1

ring_sketch = cq.Sketch().circle(outer_diameter / 2).circle(inner_radius, mode='s')
base_ring = cq.Workplane('XY').placeSketch(ring_sketch).extrude(ring_thickness)

boss_profile = (
    cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(boss_base_radius, 0)
    .lineTo(boss_base_radius, extension_height)
    .lineTo(extension_radius, extension_height)
    .lineTo(inner_radius, boss_height - taper_height)
    .lineTo(top_radius, boss_height)
    .lineTo(0, boss_height)
    .close()
)

boss = boss_profile.revolve(360)

boss_with_holes = (
    boss
    .faces('>Z')
    .workplane()
    .polarArray(radius=hole_pattern_radius, startAngle=0, angle=360, count=hole_count)
    .hole(clearance_hole_diameter)
)

ribs = (
    base_ring.faces('>Z')
    .workplane()
    .polarArray(radius=rib_center_radius, startAngle=0, angle=360, count=4)
    .rect(rib_length, rib_width)
    .extrude(rib_height, both=True)
)

result = base_ring.union(boss_with_holes).union(ribs).edges('#Z').chamfer(chamfer_size)
