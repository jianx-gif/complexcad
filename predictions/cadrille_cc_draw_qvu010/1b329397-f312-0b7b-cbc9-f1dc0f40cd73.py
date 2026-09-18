import cadquery as cq
import math
base_width = 60.0
base_height = 30.0
base_thickness = 10.0
rib_width = 12.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (base_width, 0),
        (base_width, base_height),
        (base_width - rib_width, base_height),
        (base_width - rib_width, base_height + rib_height),
        (base_width - rib_width, base_height + rib_height),
        (base_width - rib_width, base_height),
        (base_width - rib_width, base_height + rib_height),
        (0, base_height),
        (0, 0)
    ])
    .close()
    .extrude(base_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
rib = rib.faces(">Z").edges().chamfer(chamfer_size)
rib = (
    rib.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = rib
