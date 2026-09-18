import cadquery as cq
length = 80.0
trap_top_width = 30.0
trap_bottom_width = 50.0
trap_height = 40.0
circle_radius = 20.0
rib_width = 10.0
rib_height = 6.0
rib_offset = 5.0
chamfer_dist = 1.0
notch_width = 12.0
notch_depth = 5.0
notch_height = 3.0
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (length, 0),
        (length, trBase),
        (trical, trbase),
        (trical, trbase),
        (0, trbase),
    ])
    .close()
    .extrude(length)
)
rib = (
    cq.Workplane("XY")
    .rect(trical, rib_height)
    .extrude(trical)
    .translate((trical, -trical, 0))
)
rib = rib.edges("|Z").chamfer(chamfer_dist)
rib = rib.edges("|Z").chamfer(chamfer_dist)
result = base.union(rib)
