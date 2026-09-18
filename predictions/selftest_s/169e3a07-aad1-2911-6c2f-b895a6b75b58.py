import cadquery as cq

inner_wall_radius = 30
wall_thickness = 3
gap_between_walls = 2
outer_wall_base_radius = inner_wall_radius + wall_thickness + gap_between_walls
corrugation_amplitude = 3
bellows_height = 40
corrugations = 8
vent_radius = 5
rib_depth = 4
rib_width = gap_between_walls + 2  # increased overlap
rib_chamfer = 0.5
edge_chamfer = 0.8
num_ribs = 8

def corrugation_profile(base_radius, amplitude, height, steps):
    pts = [(base_radius, 0.0)]
    dz = height / steps
    for i in range(1, steps + 1):
        z = i * dz
        radius = base_radius + (amplitude if i % 2 == 1 else 0.0)
        pts.append((radius, z))
    if pts[-1][0] != base_radius:
        pts.append((base_radius, height))
    return pts

inner_profile = corrugation_profile(inner_wall_radius, corrugation_amplitude, bellows_height, corrugations)
outer_profile = corrugation_profile(outer_wall_base_radius, corrugation_amplitude, bellows_height, corrugations)

inner_wall = (
    cq.Workplane('XZ')
    .polyline(inner_profile)
    .close()
    .revolve()
)

outer_wall = (
    cq.Workplane('XZ')
    .polyline(outer_profile)
    .close()
    .revolve()
)

walls = inner_wall.union(outer_wall)

vent_cutter = cq.Workplane('XY').circle(vent_radius).extrude(bellows_height + 2)
walls = walls.cut(vent_cutter)

walls = walls.edges().chamfer(edge_chamfer)

rib = (
    cq.Workplane('XY')
    .box(rib_width, rib_depth, bellows_height)
    .translate((inner_wall_radius + wall_thickness + gap_between_walls/2, 0, bellows_height/2))
)

rib_pattern = rib
for i in range(1, num_ribs):
    angle = 360.0 * i / num_ribs
    rib_rot = rib.rotate((0,0,0), (0,0,1), angle)
    rib_pattern = rib_pattern.union(rib_rot)

walls = walls.union(rib_pattern)

result = walls