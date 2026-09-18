import cadquery as cq
overall_length = 80.0
channel_width = 30.0
channel_depth = 20.0
step_height = 10.0
wall_thickness = 5.0
hole_diameter = 6.0
hole_depth = wall_thickness
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_spacing = 20.0
mount_hole_count = 4
mount_hole_radius = (overall_length - 2 * wall_thickness) / 2
base = (
    cq.Workplane("XY")
    .rect(overall_length, channel_width)
    .extrude(channel_depth)
)
base = base.edges("|Z").chamfer(chamfer_size)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(channel_width, channel_width)
    .extrude(channel_depth)
)
base = base.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (mount_hole_radius * math.cos(math.radians(a)),
    (mount_hole_radius * math.sin(math.radians(a)))
    for a in hole_positions:
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(mount_hole_diameter)
)
result = base
