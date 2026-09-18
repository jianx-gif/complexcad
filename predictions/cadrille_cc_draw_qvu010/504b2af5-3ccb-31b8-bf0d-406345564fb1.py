import cadquery as cq
base_length = 80.0
base_width = 30.0
base_thickness = 6.0
rib_height = 4.0
rib_width = 10.0
rib_spacing = 12.0
rib_count = 6
rib_spacing = 12.0
rib_offset = 10.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 15.0
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
    rib.faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = base.union(rib)
hole_positions = [
    (-hole_spacing_x/2, -hole_spacing_y/2),
    (hole_spacing_x/2, -hole_spacing_y/2),
    (-hole_spacing_x/2, hole_spacing_y/2),
    (hole_spacing_x/2, hole_spacing_y/2),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
