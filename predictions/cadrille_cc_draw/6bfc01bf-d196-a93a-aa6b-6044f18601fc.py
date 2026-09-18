import cadquery as cq
import math
base_length = 80.0
base_width = 30.0
base_thickness = 8.0
wall_thickness = 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 3
hole_offset = 15.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
base = (
    cq.Workplane("XY")
    .circle(base_length)
    .extrude(base_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .rect(base_length, base_width)
    .cutBlind(base_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .cutBlind(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_width)
    .translate((0, 0, base_thickness))
)
base = base.union(rib)
base = (
    base
    .faces(">Z")
    .workplane()
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .extrude(-rib_width)
)
base = base.union(rib)
base = (
    base
    .faces(">Z")
    .workplane()
    .rect(base_length - 2 * wall_thickness, base_width - 2 * wall_thickness)
    .cutBlind(-base_thickness)
)
result = base
