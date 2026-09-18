import cadquery as cq
import math
base_width = 80.0
base_height = 30.0
base_thickness = 10.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 10.0
rib_spacing = 15.0
rib_count = 6
rib_count = 4
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .rect(base_width, base_height)
    .cutBlind(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
rib = (
    rib
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(-base_width/2 + wall_thickness + rib_spacing/2, 0), (base_width/2 - wall_thickness - rib_spacing/2, 0)])
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.union(rib)
result = combined
