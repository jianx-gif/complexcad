import cadquery as cq
plate_length = 80.0
plate_width = 50.0
plate_thickness = 8.0
rib_width = 4.0
rib_height = 3.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .edges("|Z")
    .chamfer(chamfer_size)
)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
rib = (
    rib.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_width)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = rib.faces(">Z").workplane()
result = rib
