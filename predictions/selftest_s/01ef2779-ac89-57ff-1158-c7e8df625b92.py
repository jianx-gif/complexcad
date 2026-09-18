import cadquery as cq

overall_length = 80
channel_width = 30
channel_depth = 20
step_height = 10
wall_thickness = 5
hole_diameter = 6
chamfer_size = 1
mount_hole_diameter = 4
mount_hole_spacing = 20

overall_width = channel_width + 2 * wall_thickness
overall_height = channel_depth + step_height
mount_hole_count = int(overall_width // mount_hole_spacing) + 1

profile = (
    cq.Sketch()
    .rect(overall_width, overall_height, mode="a")
    .rect(channel_width, channel_depth, mode="s")
)

result = (
    cq.Workplane("XY")
    .placeSketch(profile)
    .extrude(overall_length)
)

result = (
    result.faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

result = (
    result.faces(">Z")
    .workplane()
    .center(0, channel_depth + step_height / 2)
    .hole(hole_diameter)
)

result = (
    result.faces(">Z")
    .workplane()
    .rarray(mount_hole_spacing, 0, mount_hole_count, 1)
    .hole(mount_hole_diameter)
)
