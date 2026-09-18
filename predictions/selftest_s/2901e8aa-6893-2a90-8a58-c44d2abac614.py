import cadquery as cq

outlet_radius = 5.0
chute_height = 80.0
chute_max_radius = 30.0
inlet_bevel_radius = 5.0
wall_thickness = 3.0
chamfer_size = 1.0
rib_thickness = wall_thickness + 1.0
rib_inner_start = outlet_radius + 0.5
rib_start_factor = 0.4
rib_end_factor = 0.7

main_body = (
    cq.Workplane("XZ")
    .moveTo(outlet_radius, 0)
    .lineTo(outlet_radius + wall_thickness, 0)
    .lineTo(outlet_radius + wall_thickness, chute_height - inlet_bevel_radius)
    .threePointArc((outlet_radius + wall_thickness + inlet_bevel_radius, chute_height - inlet_bevel_radius/2), (outlet_radius + wall_thickness + inlet_bevel_radius, chute_height))
    .lineTo(chute_max_radius, chute_height)
    .lineTo(outlet_radius, chute_height)
    .lineTo(outlet_radius, 0)
    .close()
    .revolve()
    .faces("<Z")
    .edges()
    .chamfer(chamfer_size)
)

rib = (
    cq.Workplane("XZ")
    .moveTo(rib_inner_start, chute_height * rib_start_factor)
    .lineTo(rib_inner_start + rib_thickness, chute_height * rib_start_factor)
    .lineTo(rib_inner_start + rib_thickness, chute_height * rib_end_factor)
    .lineTo(rib_inner_start, chute_height * rib_end_factor)
    .close()
    .revolve()
)

body_with_rib = main_body.union(rib)

result = (
    body_with_rib
    .faces(">X")
    .first()
    .workplane()
    .center(chute_max_radius - wall_thickness/2, chute_height/2)
    .hole(4.0)
)
