import cadquery as cq
leaf_length = 80.0
leaf_width = 30.0
leaf_thickness = 5.0
tip_radius = 6.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_spacing = 12.0
fillet_radius = 0.8
pin_diameter = 6.0
pin_depth = 3.0
chamfer_distance = 0.5
base = (
    cq.Workplane("XY")
    .rect(leaf_length, leaf_width)
    .extrude(leaf_thickness)
)
leaf = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(pin_diameter / 2)
    .cutBlind(pin_depth)
)
leaf = (
    leaf
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(pin_diameter / 2)
    .cutBlind(pin_depth)
)
leaf = (
    leaf
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
leaf = (
    leaf
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(pin_diameter / 2)
    .cutBlind(pin_depth)
)
result = leaf
