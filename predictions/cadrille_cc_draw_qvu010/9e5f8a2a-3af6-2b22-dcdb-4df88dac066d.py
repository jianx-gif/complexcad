import cadquery as cq
plate_length = 90.0
plate_width = 90.0
plate_thickness = 5.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_count = 6
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, plate_width)
    .extrude(rib_height)
)
result = base.union(rib)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, plate_width)
    .extrude(rib_height)
)
result = result.edges("|Z").chamfer(chamfer_size)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .rarray(hole_spacing, 0, 2, 1)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z").workplane()
    .rarray(hole_spacing, 0, 2, 1)
    .hole(hole_diameter)
)
