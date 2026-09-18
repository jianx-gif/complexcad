import cadquery as cq

outer_diameter = 80.0
inner_diameter = 30.0
thickness = 12.0
rib_width = 6.0
rib_height = 4.0
hole_diameter = 6.0
hole_count = 8
hole_radius = (inner_diameter/2 + outer_diameter/2) / 2
chamfer_size = 1.0

base = (
    cq.Workplane("XY")
    .sketch()
    .circle(outer_diameter/2)
    .circle(inner_diameter/2)
    .finalize()
    .extrude(thickness)
)

rib = (
    cq.Workplane("XY")
    .sketch()
    .circle(outer_diameter/2)
    .circle((outer_diameter/2) - rib_width)
    .finalize()
    .extrude(rib_height)
)

combined = base.union(rib)

with_holes = (
    combined
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, count=hole_count, startAngle=0, angle=360)
    .hole(hole_diameter)
)

result = (
    with_holes
    .edges()
    .chamfer(chamfer_size)
)
