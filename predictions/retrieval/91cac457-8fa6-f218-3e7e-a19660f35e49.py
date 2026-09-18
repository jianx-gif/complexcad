import cadquery as cq

outer_radius = 40.0
flange_radius = 45.0
flange_thickness = 5.0
body_thickness = 12.0
hub_radius = 20.0
bore_diameter = 12.0
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_pitch = 30.0
chamfer_distance = 1.0
groove1_width = 2.0
groove1_depth = 2.0
groove2_width = 2.5
groove2_depth = 2.5

groove1_center_z = -flange_thickness - body_thickness/2 + 2.0
groove1_start_z = groove1_center_z - groove1_width/2
groove2_center_z = -flange_thickness - body_thickness/2 - 4.0
groove2_start_z = groove2_center_z - groove2_width/2

profile = (cq.Workplane('XZ')
    .moveTo(flange_radius, 0)
    .lineTo(flange_radius, -flange_thickness)
    .lineTo(outer_radius, -flange_thickness)
    .lineTo(outer_radius, groove1_start_z)
    .lineTo(outer_radius - groove1_depth, groove1_start_z)
    .lineTo(outer_radius - groove1_depth, groove1_start_z + groove1_width)
    .lineTo(outer_radius, groove1_start_z + groove1_width)
    .lineTo(outer_radius, groove2_start_z)
    .lineTo(outer_radius - groove2_depth, groove2_start_z)
    .lineTo(outer_radius - groove2_depth, groove2_start_z + groove2_width)
    .lineTo(outer_radius, groove2_start_z + groove2_width)
    .lineTo(outer_radius, -flange_thickness - body_thickness)
    .lineTo(hub_radius, -flange_thickness - body_thickness)
    .lineTo(hub_radius, 0)
    .close()
)

result = profile.revolve(360)

result = result.faces('>Z').workplane().hole(bore_diameter)

result = result.faces('>Z').workplane().polarArray(mount_hole_pitch, 0, 360, mount_hole_count).hole(mount_hole_diameter)

result = result.faces('>Z').edges().chamfer(chamfer_distance)
