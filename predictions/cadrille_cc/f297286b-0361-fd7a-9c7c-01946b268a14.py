import cadquery as cq
outer_diameter = 100.0
plate_thickness = 5.0
rib_width = 8.0
rib_height = 12.0
rib_thickness = 5.0
hole_diameter = 6.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 0.5
rib_count = 4
rib_count = 4
rib_count = 12
rib_spacing = 12.0
rib_depth = 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(plate_thickness)
)
rib_profile = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
)
rib_pattern = rib.translate((0, 0, plate_thickness))
rib_pattern = rib_pattern.union(rib)
result = (
    base.union(rib_pattern)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
)
result = result.union(rib_pattern)
result = (
    result.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
)
result = result.edges("|Z").chamfer(chamfer_size)
