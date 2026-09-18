import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_end = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, plate_width)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
base = base.union(rib)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_spacing, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
base = base.union(rib)
hole_positions = [
    (-hole_offset_from_end, -hole_spacing),
    (hole_offset_from_end, -hole_spacing),
    (hole_offset_from_end, hole_spacing),
    (-hole_offset_from_end, hole_spacing),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
result = base.union(rib)
