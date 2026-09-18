import cadquery as cq

hub_radius = 20.0
hub_height = 10.0
blade_length = 30.0
blade_root_width = 8.0
blade_tip_width = 14.0
blade_thickness = 2.0
blade_count = 6
chamfer_size = 0.5
overlap = 0.5

hub = cq.Workplane('XY').circle(hub_radius).extrude(hub_height)

blade_profile = (
    cq.Workplane('XY')
    .moveTo(hub_radius - overlap, -blade_root_width/2)
    .lineTo(hub_radius + blade_length, -blade_tip_width/2)
    .lineTo(hub_radius + blade_length, blade_tip_width/2)
    .lineTo(hub_radius - overlap, blade_root_width/2)
    .close()
)

blade = blade_profile.extrude(blade_thickness)

blades = blade
for i in range(1, blade_count):
    angle = i * 360.0 / blade_count
    blades = blades.union(blade.rotate((0, 0, 0), (0, 0, 1), angle))

result = hub.union(blades).faces('>Z').edges().chamfer(chamfer_size)
