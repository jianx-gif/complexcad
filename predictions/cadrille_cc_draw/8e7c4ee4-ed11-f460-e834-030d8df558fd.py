import cadquery as cq
outer_radius = 35.0
wall_thickness = 8.0
inner_radius = outer_radius - wall_thickness
wall_thickness = 2.0
rib_height = 12.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 4
hole_offset = wall_thickness + wall_thickness + rib_height / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
