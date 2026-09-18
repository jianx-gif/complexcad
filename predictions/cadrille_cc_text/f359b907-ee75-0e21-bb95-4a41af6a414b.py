import cadquery as cq
import math
gear_outer_radius = 45.0
gear_thickness = 12.0
bore_diameter = 30.0
num_teeth = 30
tooth_depth = 6.0
chamfer_distance = 1.0
boss_radius = 5.0
boss_height = gear_thickness
boss_count = 6
boss_radius = bore_diameter / 2.0
gear_body = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(bore_outer_radius, 0)
    .lineTo(bore_outer_radius, gear_thickness)
    .lineTo(bore_outer_radius + tooth_depth, gear_thickness)
    .lineTo(bore_outer_radius + tooth_depth, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
    .lineTo(bore_outer_radius, gear_thickness + tooth_depth)
