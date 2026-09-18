import cadquery as cq
base_length = 80.0
base_width = 40.0
base_thickness = 10.0
wall_thickness = 2.0
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_offset = 15.0
rib_width = 6.0
rib_height = 8.0
rib_spacing = 12.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(base_length, base_width)
    .cutBlind(base_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .cutBlind(-rib_height)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_width)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
base = base.union(rib)
hole_positions = [
    (-hole_spacing / 2, -hole_spacing / 2),
    (hole_spacing / 2, -hole_spacing / 2),
    (-hole_spacing / 2, hole_spacing / 2),
    (hole_spacing / 2, hole_spacing / 2),
]
base = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, base_width)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
result = base.union(rib)
