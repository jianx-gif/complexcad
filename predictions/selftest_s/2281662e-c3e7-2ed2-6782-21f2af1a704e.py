import cadquery as cq
import math
inner_hole_radius = 15.0
plate_outer_radius = 45.0
plate_thickness = 8.0
skirt_height = 3.0
skirt_radial_thickness = 5.0
outer_chamfer = 2.0
mounting_hole_diameter = 8.0
mounting_hole_offset = 30.0
mounting_hole_count = 4
slot_width = 4.0
slot_length = 12.0
slot_offset_radius = 22.0
slot_count = 6
boss_radius = inner_hole_radius + 5.0
boss_height = 2.0
boss_relief_depth = 0.4
# base profile for revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_hole_radius, 0)
    .lineTo(inner_hole_radius, plate_thickness)
    .lineTo(plate_outer_radius, plate_thickness)
    .lineTo(plate_outer_radius, plate_thickness + skirt_height)
    .lineTo(plate_outer_radius + skirt_radial_thickness, plate_thickness + skirt_height)
    .lineTo(plate_outer_radius + skirt_radial_thickness, 0)
    .lineTo(inner_hole_radius, 0)
    .close()
)
result = profile.revolve()
result = result.faces('>Z').edges().chamfer(outer_chamfer)
angles = [i * 360.0 / mounting_hole_count for i in range(mounting_hole_count)]
points = [(mounting_hole_offset * math.cos(math.radians(a)), mounting_hole_offset * math.sin(math.radians(a))) for a in angles]
result = (
    result.faces('>Z')
    .workplane()
    .pushPoints(points)
    .hole(mounting_hole_diameter)
)
slot_angles = [i * 360.0 / slot_count for i in range(slot_count)]
slot_points = [(slot_offset_radius * math.cos(math.radians(a)), slot_offset_radius * math.sin(math.radians(a))) for a in slot_angles]
result = (
    result.faces('<Z')
    .workplane()
    .pushPoints(slot_points)
    .rect(slot_width, slot_length)
    .cutBlind(-plate_thickness)
)
result = (
    result.faces('<Z')
    .workplane()
    .circle(boss_radius)
    .extrude(boss_height)
)
result = (
    result.faces('>Z')
    .workplane()
    .circle(boss_radius)
    .rect(boss_radius * 0.4, boss_relief_depth)
    .cutBlind(-boss_relief_depth)
)
