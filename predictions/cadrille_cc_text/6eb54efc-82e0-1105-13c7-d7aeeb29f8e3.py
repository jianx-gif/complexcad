import cadquery as cq
base_length = 80.0
base_width = 40.0
base_thickness = 8.0
slot_length = 40.0
slot_width = 10.0
hole_diameter = 6.0
hole_depth = 4.0
hole_spacing = 15.0
hole_count = 6
hole_grid_rows = 3
hole_grid_cols = 3
chamfer_distance = 1.0
rib_width = 6.0
rib_height = 3.0
rib_spacing = 20.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-base_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, base_width)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
hole_positions = [
    (hole_count - 1) / 2, hole_count - 10),
    (-hole_count - 1) / 2, hole_count - 10),
    (hole_count - 1) / 2, hole_count - 10),
    (-hole_count - 1) / 2, hole_count - 10),
    (hole_count - 1) / 2, hole_count - 10),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
