import cadquery as cq
arm_length = 80.0
arm_width = 20.0
arm_thickness = 10.0
base_height = 30.0
pivot_radius = 5.0
pocket_width = 12.0
pocket_height = 14.0
hole_diameter = 4.0
hole_depth = 8.0
fillet_radius = 0.8
pocket_depth = 6.0
base = (
    cq.Workplane("XY")
    .rect(arm_width, arm_length)
    .extrude(base_height)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter, depth=hole_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter, depth=hole_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter, depth=hole_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter, depth=hole_depth)
)
result = base
