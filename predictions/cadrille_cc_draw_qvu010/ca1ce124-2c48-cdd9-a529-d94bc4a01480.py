import cadquery as cq
import math
base_width = 40.0
base_height = 80.0
base_thickness = 4.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
)
base = base.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
base = base.union(rib)
base = base.faces(">Z").workplane().hole(base_thickness)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.union(rib)
base = base.faces(">Z").workplane().hole(base_thickness)
rib = (
    base.faces(">Z").workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = base.union(rib)
