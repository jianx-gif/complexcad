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
rib3 = rib
for i in range(1, rib_spacing):
    angle = i * 360.0 / rib_spacing
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
result = base.union(rib2).union(rib2)
result = result.edges("|Z").chamfer(chamfer_distance)
