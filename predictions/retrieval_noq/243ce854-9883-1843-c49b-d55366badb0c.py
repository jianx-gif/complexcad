import cadquery as cq

base_radius = 40.0
vertical_height = 80.0
wall_thickness = 8.0
shoulder_step = 20.0
chamfer_size = 2.0
tap_hole_dia = 6.0
blind_hole_dia = 4.0
blind_hole_depth = 20.0

base_hole_spacing = 30.0

profile = (
    cq.Workplane('XZ')
    .lineTo(base_radius, 0)
    .lineTo(base_radius, shoulder_step)
    .lineTo(base_radius - wall_thickness, shoulder_step)
    .lineTo(base_radius - wall_thickness, vertical_height)
    .lineTo(0, vertical_height)
    .close()
)

solid = profile.revolve(360, (0,0,0), (0,1,0))
solid = solid.edges().chamfer(chamfer_size)
# tapped holes on base (bottom face)
solid = (
    solid.faces('<Z').workplane()
    .pushPoints([
        (base_radius - wall_thickness/2, -base_hole_spacing/2),
        (base_radius - wall_thickness/2, base_hole_spacing/2)
    ])
    .hole(tap_hole_dia)
)
# blind hole on vertical leg top face
solid = (
    solid.faces('>Z').workplane()
    .center(base_radius - wall_thickness/2, 0)
    .hole(blind_hole_dia, depth=blind_hole_depth)
)

result = solid
