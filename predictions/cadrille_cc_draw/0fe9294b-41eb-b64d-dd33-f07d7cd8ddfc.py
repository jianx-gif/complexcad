import cadquery as cq
outer_radius = 20.0
inner_radius = 15.0
thickness = 15.0
rib_width = 4.0
rib_height = 8.0
rib_thickness = 3.0
hole_diameter = 6.0
hole_spacing = 20.0
hole_count = 6
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(outer_radius, outer_radius)
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
    (-hole_spacing/2, -hole_offset),
    ( hole_spacing/2, -hole_offset),
    ( hole_spacing/2, -hole_offset),
    (-hole_spacing/2, hole_offset),
    ( hole_spacing/2, hole_offset),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
