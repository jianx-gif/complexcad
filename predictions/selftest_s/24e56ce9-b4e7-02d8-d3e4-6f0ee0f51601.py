import cadquery as cq

body_height = 80
base_radius = 30
seat_start_height = 50
seat_tip_radius = 20
seat_tip_height = 70
top_radius = 20
top_height = 80
bore_radius = 8
vent_hole_radius = 4
vent_hole_height = body_height * 0.6
vent_hole_offset = base_radius * 0.7
fillet_radius = 2
flange_thickness = 10
flange_radius = 40
bolt_hole_radius = 3
bolt_pattern_radius = 30
bolt_count = 4

profile = (
    cq.Workplane("XZ")
    .lineTo(base_radius, 0)
    .lineTo(base_radius, seat_start_height)
    .lineTo(seat_tip_radius, seat_tip_height)
    .lineTo(top_radius, top_height)
    .lineTo(0, top_height)
    .close()
)

body = profile.revolve()

bore = (
    cq.Workplane("XY")
    .circle(bore_radius)
    .extrude(body_height)
)

vent = (
    cq.Workplane("XY")
    .center(vent_hole_offset, 0)
    .circle(vent_hole_radius)
    .extrude(body_height)
)

flange = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_thickness)
)

bolt_cyl = (
    cq.Workplane("XY")
    .circle(bolt_hole_radius)
    .extrude(flange_thickness + 2)
)

bolt_holes = (
    bolt_cyl.translate(( bolt_pattern_radius, 0, 0))
    .union(bolt_cyl.translate((-bolt_pattern_radius, 0, 0)))
    .union(bolt_cyl.translate((0, bolt_pattern_radius, 0)))
    .union(bolt_cyl.translate((0,-bolt_pattern_radius, 0)))
)

result = (
    body
    .cut(bore)
    .cut(vent)
    .union(flange)
    .cut(bolt_holes)
    .edges("|Z")
    .fillet(fillet_radius)
)
