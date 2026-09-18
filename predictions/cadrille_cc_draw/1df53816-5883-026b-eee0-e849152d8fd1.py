import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 8
rib_count = 6
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 4
hole_offset = 15.0
base = (
    cq.Workplane("XY")
    .rect(outer_diameter, outer_diameter)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset,  hole_offset),
    (-hole_offset,  hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
