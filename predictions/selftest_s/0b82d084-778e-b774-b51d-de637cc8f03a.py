import cadquery as cq

# Parameters
outer_diameter = 80.0
inner_diameter = 60.0
cap_height = 20.0
tab_width = 10.0
tab_height = 6.0
inner_round_radius = 12.0
snap_groove_depth = 3.0
snap_groove_width = 2.0
snap_groove_offset = 4.0
chamfer_distance = 0.5
hole_diameter = 5.0
rib_height = 4.0
rib_thickness = 2.0
rib_position_z = 10.0

# 2D profile on XZ plane
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter / 2, 0)
    .lineTo(outer_diameter / 2 + tab_width, 0)
    .lineTo(outer_diameter / 2 + tab_width, tab_height)
    .lineTo(outer_diameter / 2, tab_height)
    .lineTo(outer_diameter / 2, cap_height)
    .lineTo(inner_diameter / 2 + inner_round_radius, cap_height)
    .radiusArc((inner_diameter / 2, cap_height - inner_round_radius), inner_round_radius)
    .lineTo(inner_diameter / 2, 0)
    .close()
)

result = profile.revolve(360)

# Chamfer outer bottom edge for safety
result = result.edges("<Z").chamfer(chamfer_distance)

# Snap‑fit peripheral groove (radial cut)
snap_cutter = (
    cq.Workplane("XY")
    .center(0, cap_height - snap_groove_offset)
    .circle((outer_diameter / 2) - snap_groove_depth)
    .extrude(snap_groove_width)
)
result = result.cut(snap_cutter)

# Mounting holes on the tab (drilled radially through the tab thickness)
hole_cutter = (
    cq.Workplane("XY")
    .center(outer_diameter / 2 + tab_width / 2, 0)
    .circle(hole_diameter / 2)
    .extrude(tab_height + 2)
)
result = result.cut(hole_cutter)
result = result.cut(hole_cutter.mirror(mirrorPlane="YZ"))

# Internal rib for reinforcement (attached to inner wall)
rib = (
    cq.Workplane("XZ")
    .center(inner_diameter / 2 + rib_thickness / 2, rib_position_z)
    .rect(rib_thickness, rib_height)
    .extrude(rib_thickness)
)
result = result.union(rib)
