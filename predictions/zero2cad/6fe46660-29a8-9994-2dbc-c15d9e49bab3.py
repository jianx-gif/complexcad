import cadquery as cq
import math

outer_radius = 45.0
inner_radius = 35.0
ring_height = 15.0
chamfer_size = 1.0
knurl_count = 20
knurl_width = 4.0
knurl_height = 6.0
knurl_depth = 1.5
knurl_overlap = 0.2

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(ring_height)
    .edges()
    .chamfer(chamfer_size)
)

knurl = cq.Workplane("XY")
for i in range(knurl_count):
    angle = i * 360.0 / knurl_count
    knurl_piece = (
        cq.Workplane("XY")
        .box(knurl_width, knurl_depth, knurl_height)
        .translate((outer_radius + knurl_width / 2.0 - knurl_overlap, 0, ring_height / 2.0))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    knurl = knurl.union(knurl_piece)

result = base.union(knurl)
