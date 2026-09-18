import cadquery as cq
from types import SimpleNamespace as Measures

# Parameters
m = Measures(
    outer_radius = 40.0,
    wall_thickness = 8.0,
    block_height = 50.0,
    rib_height = 12.0,
    rib_thickness = 3.0,
    fillet_radius = 1.5,
    bolt_diameter = 4.5,
    head_diameter = 8.0,
    head_height = 4.0,
)

# Derived dimensions
m.inner_radius = m.outer_radius - m.wall_thickness

# Base revolved block with outward bulge on outer surface
base = (
    cq.Workplane("XZ")
    .moveTo(m.inner_radius, 0)
    .lineTo(m.inner_radius, m.block_height)
    .lineTo(m.outer_radius, m.block_height)
    .threePointArc((m.outer_radius + m.wall_thickness/2, m.block_height/2), (m.outer_radius, 0))
    .close()
    .revolve()
)

# Rib extending outward from outer surface, positioned mid-height
rib = (
    cq.Workplane("XY")
    .circle(m.outer_radius + m.rib_thickness)
    .circle(m.outer_radius)
    .extrude(m.rib_height)
    .translate((0, 0, m.block_height/2 - m.rib_height/2))
)

combined = base.union(rib)

# Apply fillet to all edges for safety
combined = combined.edges().fillet(m.fillet_radius)

# Add countersunk holes on the top planar face
result = (
    combined
    .faces(">Z")
    .workplane()
    .polarArray(radius=m.inner_radius + m.wall_thickness/2, startAngle=30, count=2, angle=180)
    .cboreHole(m.bolt_diameter, m.head_diameter, m.head_height)
)
