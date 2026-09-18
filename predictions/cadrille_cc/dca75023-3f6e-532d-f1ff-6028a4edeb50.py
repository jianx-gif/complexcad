import cadquery as cq
base_length = 60.0
base_width = 40.0
base_thickness = 12.0
rib_width = 12.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_count = 12
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_width)
    .translate((0, 0, base_thickness))
)
rib_pattern = rib.translate((0, 0, base_thickness))
rib_pattern = rib_pattern.union(rib)
rib_pattern = rib_pattern.faces(">Z").workplane().hole(rib_width)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_width)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_width)
rib_pattern = rib_pattern.union(rib_pattern)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_width)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_width)
rib_pattern = rib_pattern.union(rib_pattern)
result = rib_pattern
