import cadquery as cq

outer_diameter = 80.0
flange_thickness = 10.0
pocket_diameter = 30.0
pocket_depth = 6.0
hole_diameter = 5.0
hole_offset_radius = 30.0
chamfer_size = 1.0
rib_width = 6.0
rib_length = 40.0
rib_height = 4.0

base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(flange_thickness)
)

pocket = (
    base.faces(">Z")
    .workplane()
    .circle(pocket_diameter / 2)
    .cutBlind(pocket_depth)
)

holes = (
    pocket.faces(">Z")
    .workplane()
    .pushPoints([
        (hole_offset_radius, 0),
        (0, hole_offset_radius),
        (-hole_offset_radius, 0),
        (0, -hole_offset_radius),
    ])
    .hole(hole_diameter)
)

rib = (
    holes.faces(">Z")
    .workplane()
    .rect(rib_length, rib_width)
    .extrude(rib_height)
)

result = (
    rib.edges()
    .chamfer(chamfer_size)
)
