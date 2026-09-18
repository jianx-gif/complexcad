import cadquery as cq
import math
bracket_thickness = 10
triangle_radius = 45
central_hole_diameter = 20
slot_width = 8
slot_length = 30
chamfer_distance = 2
tab_length = 25
tab_width = 15
tab_thickness = bracket_thickness
slot_center1_x = triangle_radius * math.cos(math.radians(210))
slot_center1_y = triangle_radius * math.sin(math.radians(210))
slot_center2_x = triangle_radius * math.cos(math.radians(330))
slot_center2_y = triangle_radius * math.sin(math.radians(330))
base = (
    cq.Workplane('XY')
    .polygon(3, triangle_radius * 2)
    .extrude(bracket_thickness)
    .faces('>Z')
    .workplane()
    .hole(central_hole_diameter)
    .pushPoints([
        (slot_center1_x, slot_center1_y),
        (slot_center2_x, slot_center2_y)
    ])
    .rect(slot_length, slot_width)
    .cutBlind(-bracket_thickness)
    .edges('|Z')
    .chamfer(chamfer_distance)
)
# Add a mounting tab on the +X side
tab = (
    base.faces('>X')
    .workplane()
    .rect(tab_width, tab_length)
    .extrude(tab_thickness)
)
result = base.union(tab)
