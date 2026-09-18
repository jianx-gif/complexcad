import cadquery as cq
base_length = 80.0
base_width = 50.0
base_thickness = 5.0
rib_height = 20.0
rib_width = 10.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
rib = rib.translate((0, 0, base_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
hole_positions = [
    (-hole_offset, -base_width/2),
    (hole_offset, -base_width/2),
    (-hole_offset, -base_width/2),
    (hole_offset, -base_width/2),
    (hole_offset, -base_width/2),
]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
