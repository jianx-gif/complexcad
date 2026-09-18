import cadquery as cq

# Parameters
base_radius = 20.0
base_height = 10.0
shoulder_radius = 30.0
shoulder_height = 8.0
central_hole_diameter = 8.0
mount_hole_diameter = 5.0
mount_hole_offset = 12.0
chamfer_distance = 0.5

# Create stepped profile and revolve
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, base_height)
    .lineTo(shoulder_radius, base_height)
    .lineTo(shoulder_radius, base_height + shoulder_height)
    .lineTo(0, base_height + shoulder_height)
    .close()
)

result = (
    profile
    .revolve()
    .workplane()
    .hole(central_hole_diameter)
    .workplane(offset=base_height + shoulder_height)
    .pushPoints([
        (mount_hole_offset, 0),
        (-mount_hole_offset, 0),
        (0, mount_hole_offset),
        (0, -mount_hole_offset),
    ])
    .hole(mount_hole_diameter)
    .edges(">Z")
    .chamfer(chamfer_distance)
)
