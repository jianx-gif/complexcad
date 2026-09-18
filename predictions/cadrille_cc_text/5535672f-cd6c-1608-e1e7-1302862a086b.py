import cadquery as cq
plate_width = 70.0
plate_height = 100.0
plate_thickness = 8.0
rib_width = 5.0
rib_height = 12.0
rib_thickness = 4.0
chamfer = 1.0
hole_dia = 5.0
hole_spacing_x = 30.0
hole_spacing_y = 30.0
slot_width = 10.0
slot_height = 40.0
rib_spacing = 15.0
rib_thickness = 4.0
rib_height = 12.0
base = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
base = base.edges("|Z").chamfer(chamfer)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_height)
    .cutBlind(-plate_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_dia)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
result = base.union(rib)
