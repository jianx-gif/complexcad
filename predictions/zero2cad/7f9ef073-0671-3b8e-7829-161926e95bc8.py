import cadquery as cq

outer_diameter = 60.0
inner_diameter = 30.0
collar_length = 20.0
keyway_width = 5.0
keyway_depth = 4.0
fillet_radius = 0.5
rib_height = 4.0
rib_thickness = 2.0
rib_count = 4
tab_width = 10.0
tab_height = 4.0
tab_thickness = 3.0

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(collar_length)
    .hole(inner_diameter)
)

base = base.edges().fillet(fillet_radius)

keyway = (
    cq.Workplane("XY")
    .box(keyway_depth, keyway_width, collar_length)
    .translate((outer_radius - keyway_depth / 2.0, 0, 0))
)

base = base.cut(keyway)

rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_height, rib_height)
    .translate((outer_radius + rib_thickness / 2.0, 0, collar_length / 2.0))
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

base = base.union(ribs)

tab = (
    cq.Workplane("XY")
    .box(tab_thickness, tab_width, tab_height)
    .translate((outer_radius + tab_thickness / 2.0, 0, collar_length / 2.0))
)

result = base.union(tab)
