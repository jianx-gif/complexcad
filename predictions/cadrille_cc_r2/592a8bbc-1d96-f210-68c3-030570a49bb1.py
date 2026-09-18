import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_thickness = 2.0
rib_spacing = 12.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset_x = 15.0
hole_offset_y = 10.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib1 = rib.translate((0, 0, thickness - rib_height))
rib2 = rib.translate((0, 0, thickness - rib_height))
rib3 = rib.translate((0, 0, thickness - rib_height))
rib4 = rib1.translate((0, 0, thickness - rib_height))
rib5 = rib4.union(rib1).union(rib2)
hole_positions = [
    (hole_offset_x, hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (hole_offset_x, -hole_offset_y),
    (hole_offset_x, -hole_offset_y),
]
result = (
    base
    .union(hole_positions)
    .edges("|Z")
    .chamfer(chamfer_size)
)
