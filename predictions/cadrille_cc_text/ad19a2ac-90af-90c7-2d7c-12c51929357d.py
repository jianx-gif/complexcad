import cadquery as cq
base_radius = 35.0
outer_radius = 30.0
base_thickness = 5.0
inner_radius = 20.0
socket_height = 40.0
csk_shank_diameter = 5.0
csk_angle = 90.0
fillet_radius_internal = 3.0
pocket_width = 4.0
pocket_height = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, base_thickness)
    .lineTo(inner_radius, base_thickness)
    .lineTo(inner_radius, base_thickness + socket_height)
    .lineTo(outer_radius, base_thickness + socket_height)
    .lineTo(outer_radius, base_thickness)
    .lineTo(0, base_thickness)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(csk_shank_diameter)
solid = solid.faces(">Z").workplane().cskHole(csk_head_diameter, csk_head_diameter, csk_angle, csk_angle)
solid = solid.faces(">Z").workplane().cskHole(pocket_width, pocket_height, csk_head_diameter, csk_angle, csk_angle)
solid = solid.faces(">Z").workplane().cskHole(pocket_width, csk_head_diameter, csk_angle, csk_head_diameter, csk_angle)
solid = solid.faces(">Z").workplane().cskHole(pocket_width, csk_shank_diameter, csk_head_diameter, csk_angle, csk_angle)
result = solid
