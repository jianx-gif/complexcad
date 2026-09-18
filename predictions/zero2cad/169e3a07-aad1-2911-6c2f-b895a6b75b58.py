import cadquery as cq

outer_diameter = 80.0
wall_thickness = 5.0
bellows_height = 50.0
num_convolutions = 4
rib_count = 8
rib_width = 4.0
rib_height = 6.0
rib_thickness = 2.0
fillet_radius = 0.2

inner_radius = (outer_diameter / 2) - wall_thickness
outer_radius = outer_diameter / 2
conv_height = bellows_height / (num_convolutions * 2)

points = []
points.append((inner_radius, 0))
for i in range(num_convolutions * 2):
    radius = outer_radius if i % 2 == 0 else inner_radius
    z = (i + 1) * conv_height
    points.append((radius, z))
points.append((inner_radius, bellows_height))

profile = cq.Workplane("XZ").polyline(points).close()
bellows = profile.revolve()
bellows = bellows.edges().fillet(fillet_radius)

rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_width, rib_height)
    .translate((outer_radius - rib_thickness / 2, 0, bellows_height / 2))
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = bellows.union(ribs)
