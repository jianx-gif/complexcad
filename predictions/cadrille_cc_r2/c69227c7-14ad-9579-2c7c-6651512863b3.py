import cadquery as cq
outer_diameter = 30.0
inner_diameter = 20.0
thickness = 10.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 6
hole_radius = hole_diameter / 2.0
rib_width = 8.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 6
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
hole_positions = [
    (hole_count, hole_count),
    (-hole_count, hole_count),
    (-hole_count, -hole_count),
    (-hole_count, -hole_count),
    (-hole_count, -hole_count),
    (-hole_count, -hole_count),
    (-hole_count, -hole_count),
    (-hole_count, -hole_count),
    (-hole_count, -hole_count),
    (-hole_count, -hole_count),
    (-hole_count, -hole_count),
    (-hole_count, -hole_count),
    (-hole_count, -hole_count),
    (-hole_count, -hole_count),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
    .translate((0, 0, thickness - rib_thickness))
)
combined = combined.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
result = combined
