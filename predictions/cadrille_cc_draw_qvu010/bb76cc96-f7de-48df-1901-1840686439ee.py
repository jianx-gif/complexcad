import cadquery as cq
bracket_length = 80.0
bracket_width = 30.0
bracket_thickness = 8.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
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
    .translate((0, bracket_width/2 + rib_width/2, 0))
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
