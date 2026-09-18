import cadquery as cq

outer_diameter = 60.0
inner_diameter = 30.0
collar_width = 15.0
set_screw_diameter = 6.0
set_screw_head_diameter = 12.0
set_screw_head_depth = 2.0
chamfer_size = 1.0
rib_width = 5.0
rib_height = 3.0
rib_count = 4
keyway_width = 6.0
keyway_depth = 3.0
keyway_length = 20.0

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
set_screw_offset = (inner_radius + outer_radius) / 2.0

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(collar_width)
)

base = base.edges().chamfer(chamfer_size)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(collar_width)
)

ribs = cq.Workplane("XY")
for i in range(rib_count):
    angle = i * 360.0 / rib_count
    ribs = ribs.union(
        rib.rotate((0, 0, 0), (0, 0, 1), angle)
        .translate((0, outer_radius - rib_height / 2.0, 0))
    )

base = base.union(ribs)

base = (
    base.faces(">Z")
    .workplane()
    .center(set_screw_offset, 0)
    .cboreHole(set_screw_diameter, set_screw_head_diameter, set_screw_head_depth)
)

keyway = (
    cq.Workplane("XZ")
    .center(inner_radius - keyway_depth / 2.0, 0)
    .rect(keyway_width, keyway_length)
    .extrude(keyway_depth)
)

result = base.cut(keyway)
