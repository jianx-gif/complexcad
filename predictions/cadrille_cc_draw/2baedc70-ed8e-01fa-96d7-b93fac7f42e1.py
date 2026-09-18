import cadquery as cq
import math
base_radius = 20.0
base_height = 5.0
base_thickness = 5.0
rib_height = 3.0
rib_width = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
rib_count = 6
rib_spacing = 12.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.union(rib)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.union(rib)
base = base.edges("|Z").chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.union(rib)
base = base.edges(">Z").chamfer(chamfer_size)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.union(rib)
result = base
