import cadquery as cq

# Core dimensions
knob_outer_radius = 30.0
rim_height = 5.0
hub_step1_radius = 20.0
hub_step1_height = 8.0
hub_step2_radius = 12.0
hub_step2_height = 12.0
total_height = rim_height + hub_step1_height + hub_step2_height

# Knurl parameters
knurl_depth = 1.0
knurl_width = 2.0
knurl_pitch = 3.0
knurl_count = 12

# Shaft (central bore) parameters
shaft_radius = 5.0

# Mounting hole parameters
mount_hole_diameter = 4.0
mount_hole_spacing = 40.0

# Side boss (rib) parameters
boss_radius = 3.0
boss_height = 6.0

# Chamfer
chamfer_size = 0.5

# 2D profile for revolve (radius vs Z)
profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(knob_outer_radius, 0)
    .lineTo(knob_outer_radius, rim_height)
    .threePointArc((knob_outer_radius + 4, rim_height + 2), (hub_step1_radius, rim_height + hub_step1_height))
    .lineTo(hub_step2_radius, rim_height + hub_step1_height + hub_step2_height)
    .lineTo(0, total_height)
    .close()
)

# Revolve around Z axis
result = profile.revolve()

# Central shaft bore
result = result.faces("<Z").workplane().hole(2 * shaft_radius)

# Top mounting holes (pattern on top face)
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diameter)
)

# Knurl pattern on top face using polar array of shallow pockets
knurl_radius = (hub_step1_radius + hub_step2_radius) / 2
result = (
    result
    .faces(">Z")
    .workplane()
    .polarArray(radius=knurl_radius, count=knurl_count, startAngle=0, angle=360)
    .rect(knurl_depth, knurl_width)
    .cutBlind(-knurl_pitch)
)

# Side boss added as separate cylinder and fused
boss = (
    cq.Workplane("XY")
    .center(hub_step2_radius + boss_radius, total_height/2)
    .circle(boss_radius)
    .extrude(boss_height)
)
result = result.union(boss)

# Chamfer outer rim edge
result = result.edges(">Z").chamfer(chamfer_size)
