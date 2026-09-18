import cadquery as cq

cap_height = 30.0
cap_outer_radius = 15.0
flange_height = 12.0
flange_base_radius = 17.0
flange_top_radius = 28.0
inner_radius = 12.0
inner_cavity_depth = 24.0
notch_angle = 30.0
notch_height = 6.0
chamfer_len = 1.0
tab_width = 10.0
tab_height = 5.0
tab_thickness = 3.0

profile = (
    cq.Workplane("XY")
    .lineTo(cap_outer_radius, 0)
    .lineTo(cap_outer_radius, cap_height)
    .lineTo(flange_base_radius, cap_height)
    .lineTo(flange_top_radius, cap_height + flange_height)
    .lineTo(0, cap_height + flange_height)
    .close()
)
base = profile.revolve()

inner_cyl = cq.Workplane("XY").cylinder(inner_cavity_depth, inner_radius)
result = base.cut(inner_cyl)

# External mounting tab, positioned to intersect cap side
tab_center_x = cap_outer_radius - tab_thickness / 2.0

tab = (
    cq.Workplane("XY")
    .center(tab_center_x, cap_height / 2.0)
    .rect(tab_thickness, tab_height)
    .extrude(tab_width)
)
result = result.union(tab)

# Pressure‑relief notch via limited‑angle revolve cut
result = (
    result.workplane(offset=cap_height + flange_height / 2.0)
    .moveTo(flange_base_radius, -notch_height / 2.0)
    .lineTo(flange_top_radius, -notch_height / 2.0)
    .lineTo(flange_top_radius, notch_height / 2.0)
    .close()
    .revolve(notch_angle, combine='cut')
)

# Chamfer top perimeter edge for safety
result = result.edges(">Z").chamfer(chamfer_len)
