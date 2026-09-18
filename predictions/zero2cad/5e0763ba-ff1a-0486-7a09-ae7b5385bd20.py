import cadquery as cq

arm_length = 80.0
arm_width = 30.0
arm_thickness = 12.0
taper_ratio = 0.5
taper_length = 20.0
pocket_width = 15.0
pocket_depth = 6.0
pocket_offset = 30.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 3
chamfer_size = 1.0

base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_length, 0),
        (arm_length, arm_width * taper_ratio),
        (0, arm_width),
    ])
    .close()
    .extrude(arm_thickness)
)

pocket = (
    base.faces(">Z")
    .workplane()
    .center(pocket_offset, arm_width / 2)
    .rect(pocket_width, pocket_depth)
    .cutBlind(pocket_depth)
)

holes = (
    pocket.faces(">Y")
    .workplane()
    .center(arm_length / 2, 0)
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)

result = (
    holes.edges()
    .chamfer(chamfer_size)
)
