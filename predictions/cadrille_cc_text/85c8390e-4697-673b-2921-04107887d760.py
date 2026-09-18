import cadquery as cq
gear_diameter = 80.0
gear_length = 30.0
bearing_outer_dia = 40.0
bearing_inner_dia = 20.0
tooth_height = 5.0
cut_width = 10.0
cut_depth = 6.0
cut_thickness = 2.0
cut_spacing_angle = 30.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .circle(gear_outer_dia / 2)
    .extrude(gear_length)
)
base = (
    base.faces(">Z")
    .workplane()
    .circle(bearing_outer_dia / 2)
    .cut(cut_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .circle(bearing_inner_dia / 2)
    .cut(cut_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .circle(cut_thickness)
    .cut(cut_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=gear_diameter / 2 - cut_width / 2, startAngle=0, angle=360, count=cut_spacing_angle)
    .circle(cut_thickness)
    .cut(cut_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=hole_outer_dia / 2 - cut_width / 2 - cut_width / 2, startAngle=0, angle=360, count=6)
    .rect(cut_width, cut_depth)
    .cutBlind(-cut_thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)
result = base
