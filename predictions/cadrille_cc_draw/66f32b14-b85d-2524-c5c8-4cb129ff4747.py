import cadquery as cq
plate_length = 80.0
plate_width = 80.0
plate_thickness = 5.0
rib_height = 30.0
rib_width = 10.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_x = 15.0
hole_offset_y = 10.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = (
    rib.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = (
    rib.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = base.union(rib)
result = (
    result.faces(">Z").workplane()
    .rarray(hole_spacing, 0, hole_spacing, 1, center=True)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z").workplane()
    .rarray(hole_spacing, 0, hole_spacing, 1, center=True)
    .hole(hole_diameter)
)
