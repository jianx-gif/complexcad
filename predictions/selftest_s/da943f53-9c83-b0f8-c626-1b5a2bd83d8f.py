import cadquery as cq

# Dimensions (scaled, max 100 units)
module_size = 2.0
num_teeth = 30
gear_thickness = 12.0
addendum = module_size
dedendum = 1.25 * module_size
pitch_diameter = module_size * num_teeth  # 60
pitch_radius = pitch_diameter / 2.0  # 30
outer_radius = pitch_radius + addendum  # 32
root_radius = pitch_radius - dedendum  # 27.5
gear_sector_angle = 360.0 / num_teeth
chamfer_size = 0.5
# Relief pocket dimensions
pocket_width = 20.0
pocket_depth = 10.0
pocket_height = 4.0
# Shaft/housing dimensions
shaft_radius = 5.0
shaft_extend = 20.0
shaft_length = gear_thickness + shaft_extend
set_screw_diameter = 3.0
# Tooth tip chamfer radius
tip_chamfer = 0.5

# Base conical gear blank using Solid.makeCone
cone_solid = cq.Solid.makeCone(gear_thickness, outer_radius, root_radius)
gear_blank = cq.Workplane('XY').add(cone_solid)

# Single tooth profile on XZ plane
tooth_profile = (
    cq.Workplane('XZ')
    .moveTo(root_radius, 0)
    .lineTo(outer_radius - tip_chamfer, 0)
    .threePointArc((outer_radius, 0), (outer_radius, tip_chamfer))
    .lineTo(outer_radius, gear_thickness - tip_chamfer)
    .threePointArc((outer_radius, gear_thickness), (outer_radius - tip_chamfer, gear_thickness))
    .lineTo(root_radius, gear_thickness)
    .close()
)

# Revolve to create a single tooth sector
single_tooth = tooth_profile.revolve(angleDegrees=gear_sector_angle)

# Cut teeth around Z axis using loop
gear_with_teeth = gear_blank
for i in range(num_teeth):
    angle = i * gear_sector_angle
    gear_with_teeth = gear_with_teeth.cut(single_tooth.rotate((0, 0, 0), (0, 0, 1), angle))

# Add relief pocket on outer face
gear_with_pocket = (
    gear_with_teeth
    .faces('>Z')
    .workplane()
    .rect(pocket_width, pocket_depth)
    .cutBlind(pocket_height)
)

# Add central set screw hole
gear_with_hole = (
    gear_with_pocket
    .faces('>Z')
    .workplane()
    .hole(set_screw_diameter)
)

# Chamfer all suitable edges
gear_chamfered = (
    gear_with_hole
    .edges()
    .chamfer(chamfer_size)
)

# Shaft housing extending beyond gear
shaft_housing = (
    cq.Workplane('XY')
    .circle(shaft_radius)
    .extrude(shaft_length)
)

# Combine gear and shaft housing
result = gear_chamfered.union(shaft_housing)
