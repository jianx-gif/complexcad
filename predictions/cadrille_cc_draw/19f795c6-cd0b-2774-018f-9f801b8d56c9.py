import cadquery as cq
import math
base_length = 80.0
base_width = 30.0
base_thickness = 6.0
wall_thickness = 2.0
rib_width = 10.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 8
rib_count = 4
rib_offset = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(base_length - 2 * wall_thickness, rib_width)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
base = base.union(rib)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, base_thickness))
)
base = base.union(rib)
base = (
    base.faces(">Z").workplane()
    .hole(rib_count)
    .edges("|Z")
    .chamfer(chamfer_size)
)
result = base
