import cadquery as cq

outer_diameter = 80.0
inner_diameter = 55.0
thickness = 8.0
fillet_radius = 2.0
blind_hole_diameter = 20.0
blind_hole_depth = 6.0
rib_width = 4.0
rib_height = 2.0
rib_count = 6
tab_width = 10.0
tab_height = 6.0
tab_thickness = 3.0
tab_count = 4

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
blind_hole_radius = blind_hole_diameter / 2.0

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)

base = base.faces(">Z").edges().fillet(fillet_radius)

base = (
    base.faces(">Z")
    .workplane()
    .circle(blind_hole_radius)
    .cutBlind(blind_hole_depth)
)

rib = (
    cq.Workplane("XY")
    .circle(inner_radius + rib_width)
    .circle(inner_radius)
    .extrude(rib_height)
    .translate((0, 0, thickness))
)

result = base.union(rib)

for i in range(tab_count):
    angle = i * 360.0 / tab_count
    tab = (
        cq.Workplane("XY")
        .center(outer_radius + tab_thickness / 2.0, 0)
        .rect(tab_width, tab_thickness)
        .extrude(tab_height)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(tab)
