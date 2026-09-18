import cadquery as cq
base_length = 80.0
base_width = 50.0
base_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 1.0
rib_count = int((base_width - rib_spacing) // rib_spacing)
rib_length = base_length - 2 * rib_spacing
rib_width = base_width - 2 * rib_spacing
rib_height = base_thickness - 2 * rib_width
rib_count = int((base_width - rib_spacing) // rib_spacing)
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_length)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
rib = rib.union(rib)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
]
result = (
    base.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
