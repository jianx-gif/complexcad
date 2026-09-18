import cadquery as cq
from types import SimpleNamespace as Params

p = Params(
    outer_radius = 30.0,
    inner_hole_radius = 12.0,
    spacer_length = 60.0,
    rib_height = 12.0,
    rib_thickness = 4.0,
    rib_depth = 8.0,
    rib_spacing_angle = 60.0,
    chamfer_distance = 1.0,
)

# Base revolved cylinder
base_profile = (
    cq.Workplane('XZ')
    .moveTo(p.inner_hole_radius, 0)
    .lineTo(p.inner_hole_radius, p.spacer_length)
    .lineTo(p.outer_radius, p.spacer_length)
    .lineTo(p.outer_radius, 0)
    .close()
)
base = base_profile.revolve(360)

# Central through-hole
hole = cq.Workplane('XY').circle(p.inner_hole_radius).extrude(p.spacer_length)
solid = base.cut(hole)

# Rib geometry placed at outer radius on +X side
rib = (
    cq.Workplane('XY')
    .transformed(offset=(p.outer_radius, 0, 0))
    .rect(p.rib_thickness, p.rib_height)
    .extrude(p.rib_depth)
)

# Create array of ribs by rotation around Z axis
num_ribs = int(360 / p.rib_spacing_angle)
combined = solid
for i in range(num_ribs):
    angle = i * p.rib_spacing_angle
    rib_rotated = rib.rotate((0,0,0), (0,0,1), angle)
    combined = combined.union(rib_rotated)

# Chamfer outer vertical edges
result = combined.edges('|Z and >X').chamfer(p.chamfer_distance)
