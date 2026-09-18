import cadquery as cq
outer_diameter = 80.0
inner_diameter = 60.0
thickness = 10.0
rib_height = 8.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 4
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 30.0
hole_offset = 10.0
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
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib2 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib3 = rib
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    rib = (
        cq.Workplane("XY")
        .rect(rib_width, rib_height)
        .extrude(thickness)
        .translate((0, 0, thickness))
    )
    rib2 = rib
    .translate((0, 0, thickness))
    .rotate((0, 0, 0), (0, 0, 1), angle)
    .translate((0, 0, thickness))
)
result = base.union(rib).union(rib2).union(rib1).union(rib2)
result = result.edges("|Z").chamfer(chamfer_distance)
