import cadquery as cq
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 20.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 10.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, bracket_width)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, bracket_thickness))
)
combined = base.union(rib)
hole_positions = [
    (-hole_spacing / 2, hole_offset),
    (hole_spacing / 2, hole_offset),
    (-hole_spacing / 2, hole_offset),
    (hole_spacing / 2, hole_offset),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
