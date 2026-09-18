import cadquery as cq
outer_diameter = 80
wall_thickness = 3
cap_height = 20
snap_thickness = 2
snap_width = 5
snap_depth = 4
snap_count = 6
chamfer_size = 0.5
groove_depth = 1.0
groove_width = 2.0
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
slot_z_center = cap_height * 0.6
slot_center_x = inner_radius + (wall_thickness + snap_depth) / 2.0
profile = (cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, cap_height)
    .lineTo(inner_radius, cap_height)
    .lineTo(inner_radius, 0)
    .close())
cap = profile.revolve()
cap = cap.edges('>Z').chamfer(chamfer_size)
groove = (cq.Workplane('XY')
    .circle(outer_radius - wall_thickness / 2.0)
    .extrude(groove_depth)
    .translate((0, 0, cap_height - groove_depth)))
cap = cap.cut(groove)
slot_base = (cq.Workplane('XY')
    .center(slot_center_x, 0)
    .rect(wall_thickness + snap_depth, snap_width)
    .polarArray(count=snap_count, radius=slot_center_x, startAngle=0, angle=360))
slot = slot_base.extrude(snap_thickness).translate((0, 0, slot_z_center - snap_thickness / 2.0))
result = cap.cut(slot)
