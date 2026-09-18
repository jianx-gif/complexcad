import cadquery as cq
import math

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

def gear_profile(t, base_radius, tip_radius, tooth_count):
    segment = int((t / (2*math.pi)) * tooth_count)
    if segment % 2 == 0:
        return epicycloid(t, tip_radius, tip_radius - base_radius)
    else:
        return hypocycloid(t, base_radius, base_radius - tip_radius)

# Core dimensions
gear_teeth = 24
module = 2.0
pitch_diameter = module * gear_teeth
gear_height = 12.0
helix_angle_deg = 15.0
helix_angle_rad = math.radians(helix_angle_deg)
helix_twist = gear_height * math.tan(helix_angle_rad) * 360.0 / (math.pi * pitch_diameter)
base_radius = pitch_diameter/2 - 2.0
tip_radius = pitch_diameter/2 + 2.0
hub_radius = 8.0
hub_fillet_radius = 1.0
center_hole_diameter = 6.0
mounting_hole_diameter = 2.5
mounting_hole_offset = hub_radius + 5.0
keyway_width = 1.0
keyway_length = hub_radius * 1.5
pocket_width = 15.0
pocket_length = 5.0
pocket_depth = 2.0

# Gear profile curve
gear_curve = (
    cq.Workplane('XY')
    .parametricCurve(lambda t: gear_profile(t, base_radius, tip_radius, gear_teeth))
)
gear_body = gear_curve.twistExtrude(gear_height, helix_twist)
# Hub cylinder
hub = cq.Workplane('XY').circle(hub_radius).extrude(gear_height)
# Union gear and hub, then fillet hub‑gear transition
pre_fillet = gear_body.union(hub)
filleted = pre_fillet.edges().fillet(hub_fillet_radius)
# Mounting holes around hub
with_mounts = filleted.faces('>Z').workplane().pushPoints([
    (mounting_hole_offset, 0),
    (-mounting_hole_offset, 0),
    (0, mounting_hole_offset),
    (0, -mounting_hole_offset)
]).hole(mounting_hole_diameter)
# Keyway slot through hub
with_key = with_mounts.faces('>Z').workplane().center(0,0).rect(keyway_length, keyway_width).cutBlind(-gear_height)
# Pocket on outer rim
with_pocket = with_key.faces('>Z').workplane().center(0,0).rect(pocket_width, pocket_length).cutBlind(-pocket_depth)
# Central clearance hole
result = with_pocket.faces('>Z').workplane().hole(center_hole_diameter)
