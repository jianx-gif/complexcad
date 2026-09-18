import cadquery as cq
outer_length = 80.0
outer_width = 50.0
outer_height = 20.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(outer_length, outer_width)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(outer_length - 2 * wall_thickness, outer_width - 2 * wall_thickness)
    .extrude(outer_height)
)
rib = rib.translate((0, 0, outer_height - outer_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
rib = rib.translate((0, 0, outer_height - rib_height))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (-hole_offset, -hole_offset),
    (-hole_offset, -hole_offset),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
