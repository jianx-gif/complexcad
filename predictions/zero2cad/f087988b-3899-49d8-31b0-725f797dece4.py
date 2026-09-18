import cadquery as cq

outer_diameter = 80.0
inner_diameter = 30.0
ring_thickness = 10.0
boss_height = 8.0
chamfer_distance = 1.0
slot_width = 5.0
slot_length = 12.0
slot_depth = 4.0
slot_count = 6
slot_radius = (inner_diameter/2 + outer_diameter/2) / 2

base = (
    cq.Workplane("XY")
    .circle(outer_diameter/2)
    .extrude(ring_thickness)
    .faces(">Z")
    .workplane()
    .circle(inner_diameter/2)
    .cutBlind(ring_thickness)
)

boss = (
    cq.Workplane("XY")
    .circle(inner_diameter/2)
    .extrude(boss_height)
    .translate((0, 0, ring_thickness))
)

result = base.union(boss)

result = result.edges().chamfer(chamfer_distance)

result = (
    result
    .faces(">Z")
    .workplane()
    .polarArray(radius=slot_radius, count=slot_count, startAngle=0, angle=360)
    .rect(slot_width, slot_length)
    .cutBlind(slot_depth)
)
