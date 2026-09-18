import cadquery as cq

bore_diameter = 23.0
collar_base_length = 15.0
shoulder_length = 10.0
step_diameter = 35.0
outer_diameter = 60.0
set_screw_diameter = 4.0
set_screw_head_diameter = 7.0
set_screw_head_depth = 3.0
set_screw_axial_position = collar_base_length + shoulder_length/2.0
chamfer_size = 0.8
fillet_radius = 0.5

bore_radius = bore_diameter/2.0
step_radius = step_diameter/2.0
outer_radius = outer_diameter/2.0
total_length = collar_base_length + shoulder_length
extra_height = 5.0

# Build revolved profile
solid = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(bore_radius, 0)
    .lineTo(bore_radius, collar_base_length)
    .lineTo(step_radius, collar_base_length)
    .lineTo(step_radius, total_length)
    .lineTo(outer_radius, total_length)
    .lineTo(outer_radius, total_length + extra_height)
    .lineTo(0, total_length + extra_height)
    .close()
    .revolve()
    .edges("<Z")
    .chamfer(chamfer_size)
    .edges(">Z")
    .fillet(fillet_radius)
)

# Counterbore (head seat) oriented radially
counterbore = (
    cq.Workplane("XY")
    .circle(set_screw_head_diameter/2.0)
    .extrude(set_screw_head_depth)
    .rotate((0,0,0), (0,1,0), 90)
    .translate((outer_radius - set_screw_head_depth/2.0, set_screw_axial_position, 0))
)

# Through hole for set screw shaft
through_hole = (
    cq.Workplane("XY")
    .circle(set_screw_diameter/2.0)
    .extrude(outer_radius*2)
    .rotate((0,0,0), (0,1,0), 90)
    .translate((outer_radius - set_screw_head_depth, set_screw_axial_position, 0))
)

result = solid.cut(counterbore).cut(through_hole)
