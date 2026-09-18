import cadquery as cq

leaf_length = 80.0
leaf_width = 30.0
leaf_thickness = 6.0
hinge_radius = 6.0
hinge_offset = 10.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_count = 3
hole_depth = leaf_thickness - 1.0
chamfer_size = 0.5
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 20.0
tab_length = 20.0
tab_width = 10.0
tab_thickness = 4.0

base = (
    cq.Workplane("XY")
    .rect(leaf_length, leaf_width)
    .extrude(leaf_thickness)
)

hinge_cut = (
    base.faces(">Z")
    .workplane()
    .center(leaf_length/2 - hinge_offset, 0)
    .circle(hinge_radius)
    .cutBlind(-leaf_thickness)
)

hole_positions = [
    (leaf_length/2 - hinge_offset - (hole_count-1)*hole_spacing/2 + i*hole_spacing, 0)
    for i in range(hole_count)
]

with_holes = (
    hinge_cut.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, depth=hole_depth)
)

rib_count = int((leaf_length - 2*hinge_offset) // rib_spacing)
rib_positions = [
    (hinge_offset + rib_spacing/2 + i*rib_spacing, 0)
    for i in range(rib_count)
]

with_ribs = (
    with_holes.faces("<Z")
    .workplane()
    .pushPoints(rib_positions)
    .rect(rib_thickness, rib_height)
    .extrude(leaf_thickness)
)

chamfered = with_ribs.edges("|Z").chamfer(chamfer_size)

tab = (
    chamfered.faces(">X")
    .workplane()
    .rect(tab_width, tab_thickness)
    .extrude(tab_length)
)

result = chamfered.union(tab)
