import cadquery as cq
base_length = 80.0
base_width = 50.0
base_thickness = 5.0
rib_height = 30.0
rib_width = 10.0
rib_spacing = 12.0
rib_count = 8
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.translate((0, 0, base_thickness))
rib = rib.translate((0, 0, base_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(hole_diameter)
combined = combined.faces(">Z").workplane().center(0, 0).hole(hole_diameter)
result = combined
