import cadquery as cq

# Core dimensions
elbow_angle_deg = 120.0
centerline_radius = 25.4  # 1 in -> 25.4 units
wall_thickness = 3.0
outer_radius = centerline_radius + wall_thickness
inner_radius = centerline_radius
fillet_radius = 2.0
chamfer_size = 1.0

# Clearance hole on sidewall
hole_diameter = 12.7  # 0.5 in clearance
hole_angle_deg = 45.0

# Boss and mounting features
boss_radius = 6.0
boss_height = 8.0
bolt_hole_diameter = 5.0
bolt_spacing = 10.0
counterbore_diameter = 8.0
counterbore_depth = 4.0

# Internal rib for stiffness
rib_thickness = 1.0
rib_height = wall_thickness / 2
rib_offset = wall_thickness / 2

# Relief pocket on inner wall
pocket_width = 8.0
pocket_depth = 2.0
pocket_offset_angle = elbow_angle_deg / 2

# Profile for elbow (composite lines and arcs)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, centerline_radius - fillet_radius)
    .threePointArc((outer_radius, centerline_radius), (outer_radius - fillet_radius, centerline_radius))
    .lineTo(inner_radius + fillet_radius, centerline_radius)
    .threePointArc((inner_radius, centerline_radius - fillet_radius), (inner_radius, centerline_radius))
    .lineTo(inner_radius, 0)
    .close()
)

# Elbow solid by revolving the profile
elbow = profile.revolve(elbow_angle_deg)

# Safety chamfer on outer edges
elbow = elbow.edges("|Z and >X").chamfer(chamfer_size)

# Internal rib (revolve a small rectangular profile offset from inner wall)
rib_profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius + rib_offset, 0)
    .rect(rib_thickness, rib_height)
)
rib = rib_profile.revolve(elbow_angle_deg)
elbow = elbow.union(rib)

# Mounting boss near the start of the elbow (angle 0)
# Position boss at outer surface midpoint of the straight section
boss = (
    cq.Workplane("XZ")
    .center(outer_radius, centerline_radius/2)
    .circle(boss_radius)
    .extrude(boss_height)
)
# Counterbore on top of boss
counterbore = (
    cq.Workplane("XZ")
    .center(outer_radius, centerline_radius/2 + boss_height)
    .circle(counterbore_diameter/2)
    .extrude(-counterbore_depth)
)
boss = boss.union(counterbore)
# Bolt holes through boss (through entire boss height + counterbore)
bolt_holes = (
    cq.Workplane("XY")
    .center(outer_radius, centerline_radius/2)
    .pushPoints([(0, bolt_spacing/2), (0, -bolt_spacing/2)])
    .circle(bolt_hole_diameter/2)
    .extrude(boss_height + counterbore_depth + 2)
)
# Combine boss with elbow and cut bolt holes
elbow = elbow.union(boss).cut(bolt_holes)

# Relief pocket on inner wall at mid-sweep
pocket_center = (
    cq.Workplane("XY")
    .center(inner_radius + wall_thickness/2, 0)
    .rotate((0,0,0), (0,0,1), pocket_offset_angle)
)
# Create pocket solid and subtract
pocket_solid = (
    pocket_center
    .workplane()
    .rect(pocket_width, pocket_depth)
    .extrude(pocket_depth)
)
elbow = elbow.cut(pocket_solid)

# Clearance hole through sidewall at specified angle
hole = (
    cq.Workplane("XZ")
    .center(outer_radius, centerline_radius/2)
    .circle(hole_diameter/2)
    .extrude(wall_thickness*2)
    .rotate((0,0,0), (0,1,0), hole_angle_deg)
)
result = elbow.cut(hole)
