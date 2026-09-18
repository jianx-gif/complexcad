import cadquery as cq

# Parameters
outer_radius_bottom = 40.0
outer_radius_top = 30.0
wall_thickness = 5.0
cover_height = 50.0
fillet_radius = 2.0
chamfer_distance = 1.5
mount_hole_diameter = 5.0
mount_hole_count = 4
mount_hole_radius = 20.0
vent_slot_width = 4.0
vent_slot_length = 20.0
vent_slot_count = 6
vent_slot_angle_offset = 15.0
snap_tab_height = 4.0
snap_tab_thickness = 2.0
snap_tab_angle = 30.0

# Base profile for revolve (outer and inner walls)
profile = (
    cq.Workplane("XY")
    .moveTo(outer_radius_bottom, 0)
    .lineTo(outer_radius_top, cover_height)
    .lineTo(outer_radius_top - wall_thickness, cover_height)
    .lineTo(outer_radius_bottom - wall_thickness, 0)
    .close()
)

# Revolve the profile around Z axis
result = profile.revolve()

# Chamfer the bottom outer edge for deburring
result = result.faces("<Z").edges().chamfer(chamfer_distance)

# Fillet the top rim (outer edge)
result = result.faces(">Z").edges().fillet(fillet_radius)

# Add mounting holes on the top face, patterned radially
result = (
    result
    .workplane(offset=cover_height)
    .polarArray(radius=mount_hole_radius, startAngle=0, count=mount_hole_count, angle=360)
    .hole(mount_hole_diameter)
)

# Add vent slots on the top face, distributed around circumference
result = (
    result
    .workplane(offset=cover_height)
    .polarArray(radius=outer_radius_top - wall_thickness/2, startAngle=vent_slot_angle_offset, count=vent_slot_count, angle=360)
    .rect(vent_slot_length, vent_slot_width)
    .cutBlind(-wall_thickness)
)

# Add a snap‑tab feature at the bottom outer rim (integral protrusion)
snap = (
    cq.Workplane("XY")
    .moveTo(outer_radius_bottom, 0)
    .lineTo(outer_radius_bottom + snap_tab_thickness, 0)
    .lineTo(outer_radius_bottom + snap_tab_thickness, snap_tab_height)
    .lineTo(outer_radius_bottom, snap_tab_height)
    .close()
    .extrude(snap_tab_height)
    .rotate((0, 0, 0), (0, 0, 1), snap_tab_angle)
)
result = result.union(snap)

# End of modeling
