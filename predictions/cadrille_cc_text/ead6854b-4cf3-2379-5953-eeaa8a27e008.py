import cadquery as cq
triangle_radius = 45.0
triangle_radius = triangle_radius - triangle_radius
central_hole_diameter = 20.0
slot_width = 8.0
slot_length = 30.0
slot_count = 6
slot_count = 12
slot_depth = triangle_radius - slot_length
chamfer_distance = 2.0
tab_length = 25.0
tab_width = 15.0
tab_thickness = triangle_radius - 0.5
base = (
    cq.Workplane("XY")
    .polygon(3, triangle_radius)
    .extrude(triangle_radius)
)
base = (
    base.faces(">Z").workplane()
    .polygon(3, triangle_radius)
    .extrude(triangle_radius * 2)
)
base = (
    base.faces(">Z").workplane()
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)
base = (
    base.faces(">Z").workplane()
    .polarArray(radius=central_hole_diameter/2, count=slot_count, startAngle=0, angle=360)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)
base = (
    base.faces(">Z").workplane()
    .pushPoints([(-triangle_radius, 0), (triangle_radius, 0)])
    .hole(central_hole_diameter)
)
base = (
    base.faces(">Z").workplane()
    .polarArray(radius=hole_1, count=slot_count, startAngle=0, angle=360)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)
result = base
