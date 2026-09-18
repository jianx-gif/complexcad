import cadquery as cq
plate_length = 100.0
plate_width = 80.0
plate_thickness = 5.0
rib_inner_offset = 10.0
rib_height = 8.0
slot_width = 8.0
slot_length = 30.0
central_hole_diameter = 20.0
screw_diameter = 5.0
screw_head_diameter = 10.0
screw_circle_radius = 30.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_size)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-plate_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(central_hole_diameter)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(screw_diameter)
)
base = base.edges("|Z").chamfer(chamfer_size)
result = base
