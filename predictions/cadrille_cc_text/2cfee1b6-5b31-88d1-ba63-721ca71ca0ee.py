import cadquery as cq
overall_diameter = 60.0
overall_length = 30.0
wall_thickness = 2.0
groove_width = 2.0
groove_depth = 1.5
groove_depth = wall_thickness + 2.0
knurl_pitch = 4.0
knurl_height = 1.0
knurl_count = 12
chamfer_distance = 0.5
outer_radius = overall_diameter / 2.0
inner_radius = inner_radius + wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(overall_length)
    .faces(">Z")
    .workplane()
    .rect(groove_width, overall_length)
    .extrude(groove_depth)
    .faces(">Z")
    .workplane()
    .rect(knurl_pitch, overall_length)
    .extrude(knurl_height)
    .faces(">Z")
    .workplane()
    .polarArray(radius=overall_radius - groove_depth/2, count=3, startAngle=0, angle=360)
    .rect(knurl_pitch, overall_length)
    .cutBlind(-groove_depth)
    .edges("|Z")
    .chamfer(chamfer_distance)
)
knurl = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(knurl_pitch / 2.0)
    .extrude(knurl_height)
)
knurl = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(knurl_pitch, overall_length)
    .extrude(knurl_height)
)
knurl = knurl.union(knurl)
knurl = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(knurl_pitch, overall_length)
    .extrude(knurl_height)
)
knurl = knurl.union(knurl)
result = base.cut(knurl)
