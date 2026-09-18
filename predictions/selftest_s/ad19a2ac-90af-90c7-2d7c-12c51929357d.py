import cadquery as cq

base_radius = 35.0
base_thickness = 5.0
outer_radius = 30.0
inner_radius = 20.0
socket_height = 40.0
fillet_radius_internal = 3.0
csk_shank_diameter = 5.0
csk_head_diameter = 10.0
csk_angle = 90.0
pocket_width = 4.0
pocket_height = 10.0
pocket_depth = outer_radius - inner_radius - 1.0

profile = (
    cq.Workplane('XZ')
    .moveTo(base_radius, 0)
    .lineTo(base_radius, base_thickness)
    .lineTo(outer_radius, base_thickness)
    .lineTo(outer_radius, socket_height - fillet_radius_internal)
    .threePointArc((inner_radius + fillet_radius_internal, socket_height), (inner_radius, socket_height - fillet_radius_internal))
    .lineTo(inner_radius, base_thickness)
    .lineTo(base_radius, base_thickness)
    .close()
)

solid = profile.revolve()

pocket_cut = (
    cq.Workplane('XY')
    .box(pocket_depth, pocket_width, pocket_height)
    .translate((outer_radius - pocket_depth/2, 0, socket_height/2))
)

with_pocket = solid.cut(pocket_cut)

result = with_pocket.faces('>Z').cskHole(csk_shank_diameter, csk_head_diameter, csk_angle, depth=socket_height)
