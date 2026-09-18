import cadquery as cq
import math
base_length = 80.0
base_width = 30.0
base_thickness = 8.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .sketch()
    .rect(base_length, base_width)
    .finalize()
    .extrude(base_thickness)
)
base = base.edges("|Z").fillet(base_fillet)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
base = base.union(rib)
base = base.faces(">Z").workplane().hole(rib_count)
base = base.faces(">Z").workplane().hole(rib_width)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = base.union(rib)
