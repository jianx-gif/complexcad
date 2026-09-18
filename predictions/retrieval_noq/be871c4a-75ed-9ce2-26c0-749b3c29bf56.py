import cadquery as cq

web_thickness = 2.0
leg_length = 30.0
leg_width = 10.0
fillet_radius = 3.0
screw_recess_radius = 2.5
screw_recess_depth = 5.0
mount_hole_diameter = 4.0
mount_hole_offset = 15.0
rib_height = 5.0
rib_thickness = 1.5

# vertical leg
vertical = (
    cq.Workplane("XY")
    .rect(leg_width, leg_length)
    .extrude(web_thickness)
    .translate((leg_width / 2, leg_length / 2, web_thickness / 2))
)
# horizontal leg
horizontal = (
    cq.Workplane("XY")
    .rect(leg_length, leg_width)
    .extrude(web_thickness)
    .translate((leg_length / 2, leg_width / 2, web_thickness / 2))
)
# union legs to form corner
base = vertical.union(horizontal)
# apply fillet to outer edges on top face
base = base.edges("|Z and (not <Z)").fillet(fillet_radius)
# add reinforcing rib on interior of vertical leg
rib = (
    cq.Workplane("XZ")
    .rect(rib_thickness, rib_height)
    .extrude(leg_width)
    .translate((web_thickness / 2, leg_length - rib_height / 2, web_thickness / 2))
)
base = base.union(rib)
# add set screw recessed pocket on horizontal leg
screw_center_x = leg_length - 10.0
screw_center_y = leg_width / 2
base = (
    base.faces(">Z")
    .workplane()
    .center(screw_center_x, screw_center_y)
    .circle(screw_recess_radius)
    .cutBlind(screw_recess_depth)
)
# add two mounting holes on vertical leg
hole1_y = mount_hole_offset
hole2_y = leg_length - mount_hole_offset
base = (
    base.faces(">Z")
    .workplane()
    .center(leg_width / 2, hole1_y)
    .hole(mount_hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(leg_width / 2, hole2_y)
    .hole(mount_hole_diameter)
)
result = base