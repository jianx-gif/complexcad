import cadquery as cq

arm_length = 80.0
arm_width = 30.0
arm_thickness = 10.0
tip_radius = 8.0
fillet_radius = 2.0
chamfer_distance = 1.0

groove_width = 8.0
groove_depth = 6.0
groove_offset = 2.0

counterbore_diameter = 10.0
counterbore_depth = 8.0
counterbore_hole_diameter = 4.0
counterbore_offset = 12.0

mount_hole_diameter = 5.0
mount_hole_spacing = 40.0

# Base block extruded along X
base = cq.Workplane('YZ').rect(arm_width, arm_thickness).extrude(arm_length - tip_radius)
# Rounded tip as sphere
tip = cq.Workplane('XY').center(arm_length - tip_radius, 0).sphere(tip_radius)
result = base.union(tip)
# Fillet longitudinal edges
result = result.edges('|X').fillet(fillet_radius)
# Groove
groove_center_y = (arm_width/2) - groove_offset - (groove_width/2)
groove = (
    cq.Workplane('XY')
    .box(arm_length - tip_radius, groove_width, groove_depth)
    .translate(((arm_length - tip_radius)/2, groove_center_y, arm_thickness/2 - groove_depth/2))
)
result = result.cut(groove)
# Counterbore larger diameter
counterbore_big = (
    cq.Workplane('XY')
    .circle(counterbore_diameter/2)
    .extrude(counterbore_depth)
    .translate((counterbore_offset, 0, arm_thickness/2 - counterbore_depth/2))
)
# Through smaller hole
counterbore_small = (
    cq.Workplane('XY')
    .circle(counterbore_hole_diameter/2)
    .extrude(arm_thickness)
    .translate((counterbore_offset, 0, 0))
)
result = result.cut(counterbore_big)
result = result.cut(counterbore_small)
# Mounting holes (two symmetric about center line)
mount_hole_pos = (
    cq.Workplane('XY')
    .circle(mount_hole_diameter/2)
    .extrude(arm_thickness)
    .translate((arm_length/2, mount_hole_spacing/2, 0))
)
mount_hole_neg = mount_hole_pos.translate((0, -mount_hole_spacing, 0))
result = result.cut(mount_hole_pos)
result = result.cut(mount_hole_neg)
