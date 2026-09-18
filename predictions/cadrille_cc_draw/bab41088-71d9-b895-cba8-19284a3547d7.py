import cadquery as cq
outer_diameter = 40.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_diameter = inner_diameter - 2 * wall_thickness
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_count = 3
hole_offset = 10.0
rib_width = 4.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
base = (
    cq.Workplane("XY")
    .sketch()
    .rect(outer_diameter, outer_diameter)
    .circle(inner_diameter / 2)
    .finalize()
    .extrude(wall_thickness)
)
base = base.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(wall_thickness)
)
rib = rib.translate((rib_spacing, 0, 0))
rib = rib.translate((rib_spacing, 0, 0))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (hole_offset, 0),
]
for x, y in hole_positions:
    combined = (
        combined.faces(">Z")
        .workplane()
        .pushPoints(hole_positions)
        .hole(hole_diameter)
    )
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
