import cadquery as cq
bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 12.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 10.0
rib_spacing = 20.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, bracket_thickness)
    .extrude(rib_height)
    .translate((0, 0, bracket_thickness))
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, bracket_thickness)
    .extrude(rib_height)
)
combined = combined.edges("|Z").chamfer(chamfer_distance)
hole_positions = [
    (hole_offset, 0),
    (-hole_offset, 0),
    (0, hole_offset),
    (hole_offset, hole_offset),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
