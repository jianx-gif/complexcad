import cadquery as cq
import math

# Gear parameters
module = 2.0
num_teeth = 20
pitch_diameter = module * num_teeth  # approx
base_radius = pitch_diameter / 2.0
outer_radius = base_radius + module * 2.5
gear_thickness = 10.0
helix_angle_deg = 15.0  # helix angle
# Compute required twist angle for given thickness and helix angle
# tan(helix) = (lead)/(pi * pitch_diameter)
lead = math.tan(math.radians(helix_angle_deg)) * math.pi * pitch_diameter
twist_angle = (lead / pitch_diameter) * 360.0 * (gear_thickness / lead)  # total twist over thickness
# Simplify: twist per thickness = (lead / pitch_diameter) * 360
twist_angle = (lead / pitch_diameter) * 360.0

# Tooth geometry
tooth_width = (math.pi * pitch_diameter) / num_teeth * 0.5
tooth_height = module * 2.5

# Keyway parameters
keyway_width = module * 2.0
keyway_depth = gear_thickness * 0.6
keyway_offset = base_radius * 0.4  # distance from center to keyway center line
counterbore_diameter = module * 2.5
counterbore_depth = module * 1.0
chamfer_size = 0.5

# Helper function for cycloidal gear profile (reuse reference style)
def hypocycloid(t, r1, r2):
    return (
        (r1 - r2) * math.cos(t) + r2 * math.cos(r1 / r2 * t - t),
        (r1 - r2) * math.sin(t) + r2 * math.sin(-(r1 / r2 * t - t))
    )

def epicycloid(t, r1, r2):
    return (
        (r1 + r2) * math.cos(t) - r2 * math.cos(r1 / r2 * t + t),
        (r1 + r2) * math.sin(t) - r2 * math.sin(r1 / r2 * t + t)
    )

def gear_profile(t, r1=4, r2=1):
    if (-1) ** (1 + math.floor(t / (2 * math.pi) * (r1 / r2))) < 0:
        return epicycloid(t, r1, r2)
    else:
        return hypocycloid(t, r1, r2)

# Build gear with helical teeth via twistExtrude
gear_body = (
    cq.Workplane("XY")
    .parametricCurve(lambda t: gear_profile(t * 2 * math.pi, 6, 1))
    .twistExtrude(gear_thickness, twist_angle)
    .faces('>Z')
    .workplane()
    .hole(module)  # central bore
    .faces('>Z')
    .workplane()
    .rect(tooth_width, tooth_height)
    .extrude(gear_thickness)
)

# Add keyway on the front face
gear_with_key = (
    gear_body
    .faces('>Z')
    .workplane()
    .center(keyway_offset, 0)
    .rect(keyway_width, keyway_depth)
    .cutBlind(keyway_width)  # cut through part thickness
    .faces('>Z')
    .workplane()
    .center(keyway_offset, 0)
    .hole(counterbore_diameter, depth=counterbore_depth)
    .edges('|Z')
    .chamfer(chamfer_size)
)

result = gear_with_key