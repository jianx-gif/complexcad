import cadquery as cq
base_length = 80.0
base_width = 30.0
base_thickness = 6.0
rib_height = 4.0
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
    (-hole_spacing/2, -hole_offset_x),
    (hole_spacing/2, -hole_offset_y),
    (-hole_spacing/2, hole_offset_y),
    (hole_spacing/2, hole_offset_y),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
