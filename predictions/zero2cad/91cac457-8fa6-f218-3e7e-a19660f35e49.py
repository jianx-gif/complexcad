import cadquery as cq

outer_diameter = 80.0
inner_diameter = 40.0
thickness = 8.0
rib_height = 6.0
rib_width = 4.0
rib_count = 8
fillet_radius = 2.0
overlap = 0.5

outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(thickness)
)

base = base.edges().fillet(fillet_radius)

rib = (
    cq.Workplane("XY")
    .box(rib_height, rib_width, thickness)
    .translate((outer_radius + rib_height / 2.0 - overlap, 0, 0))
)

ribs = rib
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = base.union(ribs)
