import cadquery as cq
total_length = 80.0
outer_width_start = 30.0
outer_width_end = 15.0
outer_height_start = 20.0
outer_height_end = 10.0
inner_width_start = 15.0
inner_width_end = 7.0
web_thickness = 2.0
web_thickness = 5.0
web_height_end = 10.0
web_thickness = 5.0
web_spacing = 20.0
chamfer_distance = 0.2
outer = (
    cq.Workplane("XY")
    .rect(outer_width_start, outer_width_end)
    .extrude(outer_height_start)
    .edges("|Z")
    .chamfer(chamfer_distance)
)
outer = (
    cq.Workplane("XY")
    .rect(outer_width_start, outer_width_end)
    .extrude(outer_height_end)
    .translate((0, 0, outer_height_end))
)
outer = outer.cut(outer)
outer = outer.edges().chamfer(chamfer_distance)
inner_width_start = outer_width_start - 2 * web_thickness
inner_height_start = outer_height_end - 2 * web_thickness
outer = (
    cq.Workplane("XY")
    .rect(inner_width_start, inner_height_end)
    .extrude(inner_height_end)
    .translate((0, 0, outer_height_end))
)
result = outer.union(inner)
result = result.edges().chamfer(chamfer_distance)
result = result.edges().chamfer(chamfer_distance)
