import cadquery as cq
outer_width = 80.0
outer_height = 80.0
outer_height = 60.0
wall_thickness = 2.0
rib_width = 10.0
rib_height = 40.0
rib_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 30.0
hole_count = 4
hole_offset = 15.0
base = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .extrude(outer_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, outer_height)
    .extrude(outer_height)
    .translate((0, 0, outer_height))
)
rib = rib.translate((0, 0, outer_height - rib_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
