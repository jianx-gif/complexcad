import cadquery as cq

leaf_length = 80.0
leaf_width = 30.0
leaf_thickness = 5.0
tip_length = 10.0
tip_width = 12.0
split_gap = 1.5
split_length = leaf_length * 0.6
pin_hole_diameter = 6.0
pin_hole_offset = 15.0
fillet_radius = 0.8
chamfer_distance = 0.5

half_width = leaf_width / 2.0
half_tip_width = tip_width / 2.0

profile = (
    cq.Workplane("XY")
    .polyline([
        (-half_width, 0),
        (half_width, 0),
        (half_width, leaf_length - tip_length),
        (half_tip_width, leaf_length),
        (-half_tip_width, leaf_length),
        (-half_width, leaf_length - tip_length),
    ])
    .close()
)

leaf = profile.extrude(leaf_thickness)

leaf = (
    leaf.faces(">Z")
    .workplane()
    .center(0, leaf_length / 2 - split_length / 2)
    .rect(split_gap, split_length)
    .cutBlind(-leaf_thickness)
)

leaf = (
    leaf.faces(">Z")
    .workplane()
    .center(0, leaf_length - pin_hole_offset)
    .hole(pin_hole_diameter)
)

leaf = leaf.edges("|Z").fillet(fillet_radius)
leaf = leaf.edges("|X").chamfer(chamfer_distance)

result = leaf