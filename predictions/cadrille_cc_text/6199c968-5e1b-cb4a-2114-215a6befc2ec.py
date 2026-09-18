import cadquery as cq
outer_diameter = 80.0
wall_thickness = 5.0
flange_diameter = 100.0
flange_thickness = 10.0
cavity_radius = 20.0
cavity_depth = 30.0
cavity_draft_angle = 5.0
chamfer_distance = 1.5
rib_height = 3.0
rib_width = 5.0
rib_length = outer_diameter - 2 * wall_thickness
rib_count = 6
rib_count = 12
rib_start_z = wall_thickness + rib_height
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .workplane(offset=flange_thickness)
    .circle(inner_radius)
    .loft()
)
cavity = (
    cq.Workplane("XY")
    .circle(cavity_radius)
    .workplane(offset=flange_thickness)
    .circle(cavity_radius)
    .loft()
)
cavity = (
    cq.Workplane("XY")
    .box(cavity_depth, cavity_draft_angle, cavity_radius)
    .translate((0, 0, wall_thickness))
)
cavity = (
    cq.Workplane("XY")
    .box(cavity_depth, cavity_draft_angle, cavity_radius)
    .translate((outer_radius - cavity_depth/2.0, 0, cavity_radius))
)
result = base.cut(cavity)
result = result.edges().chamfer(chamfer_distance)
result = result.edges().chamfer(chamfer_distance)
result = result.faces(">Z").edges().chamfer(chamfer_distance)
