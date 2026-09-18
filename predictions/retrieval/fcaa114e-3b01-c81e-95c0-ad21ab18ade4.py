import cadquery as cq
import math

outer_half_width = 15.0
outer_half_height = 30.0
wall_thickness = 1.0
lip_extension = 2.0
lip_height = 3.0
screw_diameter = 3.0
countersink_diameter = 5.0
countersink_angle = 82.0
countersink_depth = (countersink_diameter/2)/math.tan(math.radians(countersink_angle/2))
hole_count = 6
chamfer_size = 0.3
wall_mid_radius = outer_half_width - wall_thickness/2

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_half_width, 0)
    .lineTo(outer_half_width, outer_half_height - lip_height)
    .lineTo(outer_half_width + lip_extension, outer_half_height - lip_height)
    .lineTo(outer_half_width + lip_extension, outer_half_height)
    .lineTo(outer_half_width, outer_half_height)
    .lineTo(outer_half_width - wall_thickness, outer_half_height)
    .lineTo(outer_half_width - wall_thickness, wall_thickness)
    .lineTo(wall_thickness, wall_thickness)
    .lineTo(wall_thickness, 0)
    .close()
)

solid = profile.revolve(360).edges().chamfer(chamfer_size)

result = (
    solid
    .workplane()
    .polarArray(radius=wall_mid_radius, count=hole_count, startAngle=0, angle=360)
    .cskHole(screw_diameter, countersink_depth, countersink_angle)
)
