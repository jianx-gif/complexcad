import cadquery as cq
import math
overall_diameter = 60.0
wall_thickness = 4.0
rib_height = 2.0
rib_width = 10.0
clip_height = 30.0
gap_width = 6.0
gap_depth = wall_thickness * 0.8
mount_hole_diameter = 5.0
countersink_diameter = 9.0
countersink_angle = 45.0
inner_radius = overall_diameter / 2.0 - wall_thickness
rib_start = clip_height * 0.3
rib_end = rib_start + rib_width
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius + wall_thickness, 0)
    .lineTo(inner_radius + wall_thickness, rib_start)
    .lineTo(inner_radius + wall_thickness + rib_height, rib_start)
    .lineTo(inner_radius + wall_thickness + rib_height, rib_end)
    .lineTo(inner_radius + wall_thickness, rib_end)
    .lineTo(inner_radius + wall_thickness, clip_height)
    .lineTo(inner_radius, clip_height)
    .close()
)
result = (
    profile
    .revolve()
    .workplane(offset=0, origin=(inner_radius + wall_thickness/2, 0, clip_height/2))
    .transformed(rotate=(0, 90, 0))
    .rect(gap_width, gap_depth)
    .cutThruAll()
    .faces(">Z")
    .workplane()
    .cskHole(mount_hole_diameter, countersink_diameter, countersink_angle)
)
