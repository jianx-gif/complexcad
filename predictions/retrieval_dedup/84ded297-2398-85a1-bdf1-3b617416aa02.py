import cadquery as cq

overall_length = 80.0
overall_width = 50.0
overall_height = 15.0
hinge_pin_diameter = 4.0
hinge_pin_length = 20.0
hinge_housing_dia = 6.0
hinge_housing_depth = 8.0
pocket_width = 20.0
pocket_depth = 10.0
pocket_height = 8.0
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
shell_thickness = 0.5
chamfer_size = 0.3

# Base plate
plate = (
    cq.Workplane("XY")
    .rect(overall_length, overall_width)
    .extrude(overall_height)
)

# Hinge housing cut on front face
plate = (
    plate
    .faces(">Z")
    .workplane()
    .center(-overall_length/2 + 5 + hinge_housing_dia/2, 0)
    .circle(hinge_housing_dia/2)
    .cutBlind(hinge_housing_depth)
)

# Recessed pocket on top surface
plate = (
    plate
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_depth)
    .cutBlind(pocket_height)
)

# Mounting holes pattern on top surface
plate = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing/2, 0), (mount_hole_spacing/2, 0)])
    .hole(mount_hole_diameter)
)

# Chamfer outer edges
plate = plate.edges("|Z").chamfer(chamfer_size)

# Shell the main body
main_body = plate.shell(-shell_thickness)

# Hinge pin solid
pin = (
    cq.Workplane("XY")
    .center(-overall_length/2, 0)
    .circle(hinge_pin_diameter/2)
    .extrude(hinge_pin_length)
)

# Combine pin with main body
result = main_body.union(pin)
