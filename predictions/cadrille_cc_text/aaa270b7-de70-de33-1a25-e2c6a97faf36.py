import cadquery as cq
clip_outer_radius = 35.0
clip_thickness = 5.0
arm_height = 30.0
arm_top_width = 20.0
arm_bottom_width = 10.0
arm_bottom_height = arm_height + arm_top_width
hole_diameter = 8.0
hole_center_offset = 12.0
chamfer_angle = 30.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(arm_outer_radius, 0)
    .lineTo(arm_outer_radius, arm_height)
    .lineTo(arm_top_width, arm_height)
    .lineTo(arm_top_width, arm_height + arm_height)
    .lineTo(0, arm_height + arm_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_angle)
hole_positions = [
    (hole_center_offset, 0),
    (-hole_center_offset, 0),
    (0, hole_center_offset),
    (0, -hole_center_offset),
]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(hole_diameter / 2)
    .cutBlind(-arm_height)
)
result = solid
