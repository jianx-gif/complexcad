import cadquery as cq
base_length = 80.0
base_width = 30.0
base_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (hole_offset, hole_offset),
    (-hole_offset, -hole_offset),
    (hole_offset, -hole_offset),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
