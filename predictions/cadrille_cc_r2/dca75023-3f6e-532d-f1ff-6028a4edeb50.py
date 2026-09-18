import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 5.0
rib_width = 12.0
rib_thickness = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib1 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib2 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib3 = rib.translate((0, rib_spacing, 0))
rib4 = rib.translate((0, rib_spacing, 0))
rib5 = rib4.union(rib1).union(rib4)
hole_positions = [
    ( hole_offset,  hole_offset),
    (-hole_offset,  hole_offset),
    ( hole_offset, -hole_offset),
    ( hole_offset, -hole_offset),
]
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
