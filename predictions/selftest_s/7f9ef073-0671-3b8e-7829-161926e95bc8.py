import cadquery as cq

bore_diameter = 30.0
bore_radius = bore_diameter / 2.0
outer_diameter = 60.0
outer_radius = outer_diameter / 2.0
collar_width = 20.0
groove_width = 5.0
groove_depth = 2.0
groove_offset = 4.0
fillet_radius = 0.5
tab_width = 10.0
tab_thickness = 3.0
tab_height = 4.0
slot_width = 5.0
slot_length = 15.0
slot_depth = 3.0
rib_count = 4
rib_width = 2.0
rib_thickness = 2.0
rib_height = 4.0
overlap = 0.2

# Base cylinder with bore and fillet on all edges
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(collar_width)
    .edges()
    .fillet(fillet_radius)
    .hole(bore_diameter)
)

# Split lock ring groove near outer face
groove_cyl = (
    cq.Workplane("XY")
    .circle(bore_radius - groove_depth)
    .extrude(groove_width)
    .translate((0, 0, collar_width - groove_offset - groove_width / 2))
)
result = result.cut(groove_cyl)

# Side mounting tab, slightly intersecting for fusion
tab = (
    cq.Workplane("XY")
    .box(tab_thickness, tab_width, tab_height)
    .translate((outer_radius - overlap + tab_thickness / 2, 0, collar_width / 2))
)
result = result.union(tab)

# Rectangular slot cut into outer side for weight reduction
slot = (
    cq.Workplane("XY")
    .box(slot_depth, slot_width, slot_length)
    .translate((outer_radius - slot_depth / 2, 0, (collar_width - slot_length) / 2))
)
result = result.cut(slot)

# Radial ribs, slightly intersecting for fusion
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_thickness, rib_height)
    .translate((outer_radius - overlap + rib_thickness / 2, 0, collar_width / 2))
)
for i in range(rib_count):
    angle = 360.0 / rib_count * i
    result = result.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))
