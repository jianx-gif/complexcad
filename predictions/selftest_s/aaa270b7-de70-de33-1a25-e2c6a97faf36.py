import cadquery as cq
from math import tan, radians

clip_outer_radius = 35.0
clip_thickness = 5.0
arm_height = 30.0
arm_top_width = 20.0
arm_bottom_width = 10.0
hole_diameter = 8.0
hole_center_offset = 12.0
chamfer_angle = 30.0
chamfer_distance = clip_thickness * tan(radians(chamfer_angle))

profile = (
    cq.Workplane("XZ")
    .moveTo(clip_thickness, 0)
    .lineTo(clip_outer_radius, 0)
    .lineTo(clip_outer_radius, arm_height - arm_bottom_width/2)
    .lineTo(clip_outer_radius + arm_top_width/2, arm_height)
    .lineTo(clip_outer_radius, arm_height)
    .lineTo(clip_thickness, arm_height)
    .close()
)

solid = profile.revolve(360)

hole_center_radius = clip_thickness + hole_center_offset

result = (
    solid
    .faces(">Z")
    .workplane()
    .center(hole_center_radius, 0)
    .circle(hole_diameter/2)
    .cutThruAll()
    .faces(">Z")
    .edges()
    .chamfer(chamfer_distance)
    .faces(">Z")
    .workplane()
    .center(clip_outer_radius + arm_top_width/4, arm_height/2)
    .rect(5.0, 2.0)
    .cutBlind(-2.0)
)
