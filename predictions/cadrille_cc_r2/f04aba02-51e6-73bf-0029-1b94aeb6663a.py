import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 15.0
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
rib4 = rib1.union(rib2)
rib5 = rib4
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    rib = (
        cq.Workplane("XY")
        .rect(rib_width, rib_height)
        .extrude(thickness)
        .translate((0, 0, thickness/2))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    rib = rib.rotate((0, 0, 0), (0, 0, 1), angle)
    rib = rib.rotate((0, 0, 0), (0, 0, 1), angle)
    rib = rib.translate((0, 0, thickness/2))
    rib1 = rib1.union(rib2)
result = base.union(rib1).union(rib2)
