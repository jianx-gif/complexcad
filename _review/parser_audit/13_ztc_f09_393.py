import cadquery as cq

# Parameters
module = 2.0
tooth_count = 16
pitch_diameter = module * tooth_count  # 32.0 units
base_radius = pitch_diameter / 2.0       # 16.0 units
gear_thickness = 10.0
shaft_diameter = 8.0
tooth_depth = 3.0
tooth_width = 5.0
chamfer_size = 0.5
helix_angle = 30.0  # degrees of twist over the gear thickness
notch_width = 1.0
notch_depth = 0.5
notch_offset = 0.6

# Base gear cylinder
gear_body = (
    cq.Workplane("XY")
    .cylinder(gear_thickness, base_radius)
)

# Central shaft, slightly longer for a clear joint
shaft = (
    cq.Workplane("XY")
    .cylinder(gear_thickness + 2.0, shaft_diameter / 2.0)
)

gear_with_shaft = gear_body.union(shaft)

# Single tooth profile (rectangle) positioned at outer radius
single_tooth_profile = (
    cq.Workplane("XY")
    .center(base_radius - tooth_depth, 0)
    .rect(tooth_width, tooth_depth)
)

# Helical extrusion to create a single tooth cut
single_helical_tooth = (
    single_tooth_profile
    .twistExtrude(gear_thickness, helix_angle)
)

# Notch feature: small rectangular pocket on the outer side of each tooth
single_notch = (
    cq.Workplane("XY")
    .center(base_radius - tooth_depth - notch_offset, 0)
    .box(notch_width, notch_depth, gear_thickness)
)

# Tip bevel cutter to approximate a chamfer on the tooth tip
single_tip_bevel = (
    cq.Workplane("XY")
    .center(base_radius - tooth_depth, 0)
    .box(tooth_width, chamfer_size, gear_thickness)
)

# Apply cuts for each tooth using a loop
gear_cut = gear_with_shaft
for i in range(tooth_count):
    angle_deg = i * 360.0 / tooth_count
    rotated_tooth = single_helical_tooth.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    rotated_notch = single_notch.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    rotated_bevel = single_tip_bevel.rotate((0, 0, 0), (0, 0, 1), angle_deg)
    gear_cut = gear_cut.cut(rotated_tooth).cut(rotated_notch).cut(rotated_bevel)

result = gear_cut
