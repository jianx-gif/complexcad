import cadquery as cq
plate_length = 80.0
plate_width = 30.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 8
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(plate_length, 0)
    .lineTo(plate_length, plate_width)
    .lineTo(plate_width, plate_thickness)
    .lineTo(0, plate_thickness)
    .close()
    .extrude(plate_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = base.union(rib)
result = (
    result.faces(">Z").workplane()
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z").workplane()
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z").workplane()
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)
