import cadquery as cq

outer_width = 80.0
case_height = 50.0
top_curve_radius = 10.0
wall_thickness = 2.0
base_thickness = 5.0
inner_radius = outer_width/2 - wall_thickness
outer_radius = outer_width/2
latch_width = 15.0
latch_thickness = 5.0
latch_height = 8.0
vent_hole_dia = 3.0
vent_rows = 4
vent_cols = 6
vent_margin = wall_thickness + 4.0
vent_spacing_x = (inner_radius*2 - 2*vent_margin) / (vent_cols - 1)
vent_spacing_y = (case_height - top_curve_radius - 2*vent_margin) / (vent_rows - 1)
vent_depth = case_height - top_curve_radius - vent_margin

outer_profile = (
    cq.Workplane('XZ')
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, case_height - top_curve_radius)
    .threePointArc((outer_radius - top_curve_radius, case_height), (0, case_height))
    .lineTo(outer_radius, 0)
    .close()
)

inner_profile = (
    cq.Workplane('XZ')
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, case_height - top_curve_radius)
    .threePointArc((inner_radius - top_curve_radius, case_height), (0, case_height))
    .lineTo(inner_radius, 0)
    .close()
)

outer_solid = outer_profile.revolve()
inner_solid = inner_profile.revolve()

hollow_body = outer_solid.cut(inner_solid)

base = (
    cq.Workplane('XY')
    .box(inner_radius*2, inner_radius*2, base_thickness, centered=(True, True, False))
)

body_with_base = hollow_body.union(base)

vented_body = (
    body_with_base
    .workplane(origin=(0, 0, case_height + base_thickness))
    .pushPoints([
        (vent_margin + i*vent_spacing_x, vent_margin + j*vent_spacing_y)
        for j in range(vent_rows) for i in range(vent_cols)
    ])
    .hole(vent_hole_dia, depth=vent_depth)
)

latch = (
    vented_body
    .faces('>X')
    .workplane(offset=wall_thickness)
    .rect(latch_width, latch_thickness)
    .extrude(latch_height)
)

result = latch