
import cadquery as cq
from types import SimpleNamespace as Measures

# Define dimensional parameters within 0-100 scale
m = Measures(
    base_width=60.0,          # total width of clamp base
    base_height=20.0,         # height of base plate before arm
    clamp_thickness=8.0,      # extrusion thickness (Z direction)
    arm_radius=30.0,          # radius of half-circle wrap arm
    bolt_hole_diameter=5.0,   # through hole for hex bolt
    bolt_hole_offset=0.0,     # offset from center along X (0 = centered)
    chamfer=1.2,              # edge chamfer size
    rib_width=6.0,
    rib_length=12.0,
    rib_height=4.0,
    rib_spacing=10.0,
    rib_count=3
)

# Build the 2D profile combining rectangle and half-circle arm
profile = (
    cq.Workplane("XY")
    .moveTo(-m.base_width/2, 0)
    .lineTo(-m.base_width/2, m.base_height)
    .lineTo(m.arm_radius, m.base_height)
    .radiusArc((-m.arm_radius, m.base_height), m.arm_radius)
    .lineTo(-m.base_width/2, 0)
    .close()
)

# Extrude profile to create solid clamp body
body = profile.extrude(m.clamp_thickness)

# Apply chamfer to all vertical edges
body = body.edges("|Z").chamfer(m.chamfer)

# Create through hole for hex bolt centered on base
hole = (
    body.faces(">Z").workplane()
    .center(m.bolt_hole_offset, m.base_height/2)
    .hole(m.bolt_hole_diameter)
)

# Add reinforcing ribs on underside, spaced along X
ribs = cq.Workplane("XY")
for i in range(m.rib_count):
    x_offset = -m.base_width/2 + m.rib_spacing + i * m.rib_spacing
    rib = (
        ribs
        .center(x_offset, m.rib_length/2)
        .rect(m.rib_width, m.rib_length)
        .extrude(m.rib_height)
    )
    ribs = ribs.union(rib)

# Combine ribs with main body
result = body.union(ribs)

# Subtract the bolt hole from the combined solid (hole already cut via .hole which is additive? Actually .hole cuts material)
# The previous hole operation already removed material, so final result is body with hole and ribs attached.
