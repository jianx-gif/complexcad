import cadquery as cq
outer_radius_bottom = 40.0
outer_radius_top = 30.0
wall_thickness = 5.0
cover_height = 50.0
cover_radius_bottom = outer_radius_bottom - wall_thickness
cover_radius_top = outer_radius_bottom - wall_thickness
cover_radius_top = outer_radius_bottom - wall_thickness
cover_height = cover_height - snap_tab_height
fillet_radius = 2.0
vent_slot_width = 4.0
vent_slot_length = 20.0
vent_slot_angle = 30.0
vent_slot_count = 6
vent_slot_angle = 30.0
snap_tab_thickness = 2.0
snap_tab_height = 4.0
snap_tab_angle = 30.0
mount_hole_diameter = 5.0
mount_hole_radius = 20.0
cover_radius_bottom = outer_radius_top - wall_thickness
cover_height = cover_height - snap_tab_height
cover_radius_bottom = outer_radius_top - wall_thickness
cover_radius_top = outer_radius_bottom - wall_thickness
cover_radius_top = outer_radius_bottom - wall_thickness
cover_radius_top = outer_radius_top - wall_thickness
cover_radius_top = outer_radius_top - wall_thickness
cover_radius_top = outer_radius_top - wall_thickness
cover_radius_top = outer_radius_top - wall_thickness
cover_radius_bottom = cover_radius_top - wall_thickness
cover_height = cover_height - snap_tab_height
vent_slot = (
    cq.Workplane("XY")
    .moveTo(cover_radius_bottom, 0)
    .lineTo(cover_radius_bottom, cover_height)
    .lineTo(cover_radius_top, cover_height)
    .lineTo(cover_radius_top, cover_height + snap_tab_height)
    .lineTo(cover_radius_top, cover_height + snap_tab_height)
    .lineTo(cover_radius_top, cover_height + snap_tab_height)
    .lineTo(cover_radius_top, cover_height + snap_tab_height)
    .lineTo(cover_radius_top, cover_height + snap_tab_height)
    .lineTo(cover_radius_top, cover_height + snap_tab_height)
    .lineTo(cover_radius_top, cover_height + snap_tab_height)
    .lineTo(cover_radius_top, cover_height + snap_tab_height)
    .lineTo(cover_radius_top, cover_height + snap_tab_height)
    .lineTo(0, cover_height + snap_tab_height)
    .close()
    .revolve()
)
result = cover_radius_bottom.union(cover_radius_top).edges().chamfer(cover_height)
