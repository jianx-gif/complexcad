import cadquery as cq
base_length = 80.0
base_width = 40.0
base_thickness = 15.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_width)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (-hole_spacing/2, -hole_offset),
    (hole_spacing/2, -hole_offset),
    (-hole_spacing/2, hole_offset),
    (hole_spacing/2, hole_offset),
    (hole_spacing/2, hole_offset + hole_spacing),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
