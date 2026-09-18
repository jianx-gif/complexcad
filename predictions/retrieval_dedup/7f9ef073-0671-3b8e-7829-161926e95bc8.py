import cadquery as cq, math

gear_outer_dia = 80.0
gear_pitch_dia = 70.0
hub_dia = 30.0
gear_width = 20.0
lead_angle_deg = 30.0
tooth_radial_height = 5.0
rib_width = 3.0
mount_hole_dia = 8.0
mounting_hole_dia = 4.0
mounting_hole_offset = 5.0
chamfer_distance = 1.0
teeth_count = 20

pitch_radius = gear_pitch_dia / 2.0
twist_angle = 360.0 * gear_width / (math.pi * gear_pitch_dia * math.tan(math.radians(lead_angle_deg)))

base_body = (
    cq.Workplane("XY")
    .cylinder(gear_width, pitch_radius)
    .val()
)

hub = (
    cq.Workplane("XY")
    .cylinder(gear_width, hub_dia / 2.0)
    .val()
)

tooth_profile = (
    cq.Workplane("XY")
    .rect(tooth_radial_height, rib_width)
    .translate((pitch_radius, 0, 0))
    .twistExtrude(gear_width, twist_angle)
)

tooth_array = (
    tooth_profile
    .polarArray(0, 0, 360, teeth_count)
    .val()
)

gear_assembled = (
    cq.Workplane("XY")
    .add(base_body)
    .add(tooth_array)
    .add(hub)
    .combine()
)

central_hole = (
    cq.Workplane("XY")
    .circle(mount_hole_dia / 2.0)
    .extrude(gear_width)
)

gear_with_central = gear_assembled.cut(central_hole)

hole_radius = hub_dia / 2.0 + mounting_hole_offset
hole_positions = [
    (hole_radius * math.cos(math.radians(a)), hole_radius * math.sin(math.radians(a)), 0)
    for a in (0, 90, 180, 270)
]

result = (
    cq.Workplane("XY")
    .add(gear_with_central)
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mounting_hole_dia)
    .edges("<Z")
    .chamfer(chamfer_distance)
)
