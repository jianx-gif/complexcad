import cadquery as cq
base_length = 80.0
base_width = 60.0
base_thickness = 12.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 10.0
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
rib_pattern = rib.translate((0, 0, base_thickness))
rib_pattern = rib_pattern.union(rib)
rib_pattern = rib_pattern.faces(">Z").workplane().hole(hole_diameter)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_height)
rib_pattern = rib_pattern.union(rib_pattern)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, base_width).extrude(rib_height)
rib_pattern = rib_pattern.union(rib_pattern)
rib_pattern = rib_pattern.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_height)
rib_pattern = rib_pattern.union(rib_pattern)
result = rib_pattern
