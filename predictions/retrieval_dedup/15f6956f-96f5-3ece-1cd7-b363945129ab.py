import cadquery as cq

plate_length = 80.0
plate_width = 50.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_margin = 5.0
hole_dia = 12.0
hole_depth = 6.0
chamfer_size = 0.5
tab_length = 20.0
tab_width = 10.0
tab_thickness = 4.0
intersect_offset = 0.5

rib_length = plate_width - 2 * rib_margin
rib_count = int((plate_length - rib_spacing) // (rib_width + rib_spacing))

base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)

result = base

total_span = (rib_count - 1) * (rib_width + rib_spacing)
for i in range(rib_count):
    x = -total_span / 2 + i * (rib_width + rib_spacing)
    rib = (
        cq.Workplane("XY")
        .rect(rib_width, rib_length)
        .extrude(rib_height)
        .translate((x, 0, plate_thickness - rib_height / 2))
    )
    result = result.union(rib)

result = result.union(
    result.faces(">Y")
    .workplane(offset=-intersect_offset)
    .center(plate_length / 2 - tab_length / 2, 0)
    .rect(tab_length, tab_thickness)
    .extrude(tab_width)
)

result = result.combine()

result = (
    result
    .faces(">Z")
    .workplane()
    .center(plate_length / 4, 0)
    .hole(hole_dia, hole_depth)
)
