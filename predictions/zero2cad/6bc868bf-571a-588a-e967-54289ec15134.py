import cadquery as cq

outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
bellows_length = 60.0
corrugation_count = 10
corrugation_amplitude = 3.0
fillet_radius = 0.2
boss_radius = 2.0
boss_height = 5.0
boss_offset = 5.0

segment = bellows_length / (corrugation_count * 2)
points = [(0, 0), (inner_radius, 0)]
for i in range(1, corrugation_count * 2 + 1):
    z = i * segment
    radius = inner_radius + (corrugation_amplitude if i % 2 == 1 else 0)
    points.append((radius, z))
points.append((0, bellows_length))

profile = cq.Workplane("XZ").polyline(points).close()
solid = profile.revolve()
thin = solid.shell(-wall_thickness)
thin = thin.edges().fillet(fillet_radius)

boss = (
    cq.Workplane("XY")
    .center(inner_radius - boss_offset, 0)
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, bellows_length - boss_height / 2))
)

result = thin.union(boss)
