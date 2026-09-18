import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 60.0
rib_height = 12.0
rib_width = 10.0
rib_thickness = 4.0
rib_count = 6
hole_diameter = 8.0
hole_depth = 8.0
hole_spacing = 20.0
chamfer_size = 1.0
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
    .circle(outer_radius)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_spacing, 0),
    (-hole_spacing, 0),
    (0, hole_spacing),
    (0, -hole_spacing),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
