import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_thickness = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset_x = 15.0
hole_offset_y = 10.0
chamfer_distance = 0.5
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
rib1 = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib2 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib3 = rib.translate((0, 0, thickness/2))
rib1 = rib.translate((0, 0, thickness/2))
rib2 = rib.translate((0, 0, thickness/2))
rib3 = rib.translate((0, 0, thickness/2))
rib1 = rib3.union(rib2)
rib2 = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib3 = rib1.union(rib2)
rib1 = rib3.translate((0, 0, thickness/2))
rib2 = rib1.union(rib1)
result = base.union(rib2)
