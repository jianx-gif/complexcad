import cadquery as cq

# Core dimensions
coupler_length = 80.0
radius_start = 20.0
radius_end = 12.0
fillet_radius = 2.0
boss_radius = 8.0
boss_height = 15.0

# Groove details
groove_width = 5.0
groove_depth = 3.0
groove_position = 0.0

# Mounting hole parameters
hole_diameter = 4.0
hole_offset = radius_start - 5.0
hole_z_offsets = [-coupler_length/4, coupler_length/4]

# Reinforcement rib parameters
rib_width = 10.0
rib_length = boss_radius * 2.5
rib_thickness = 2.0

# Pocket on top of boss
pocket_width = 12.0
pocket_depth = 6.0
pocket_height = 4.0

# Main lofted coupler body
loft_body = (
    cq.Workplane('XY')
    .workplane(offset=-coupler_length/2).circle(radius_start)
    .workplane(offset=coupler_length).circle(radius_end)
    .loft()
)

# Central boss cylinder
boss = (
    cq.Workplane('XY')
    .workplane(offset=0)
    .circle(boss_radius)
    .extrude(boss_height)
)

combined = loft_body.union(boss)

# Annular groove (ring) cut
ring = (
    cq.Workplane('XY')
    .workplane(offset=groove_position)
    .circle(radius_start)
    .circle(radius_start - groove_depth)
    .extrude(groove_width)
)
combined = combined.cut(ring)

# Add mounting holes through side walls
for z in hole_z_offsets:
    hole = (
        cq.Workplane('XY')
        .workplane(offset=z)
        .center(hole_offset, 0)
        .circle(hole_diameter/2)
        .extrude(coupler_length * 1.2)
    )
    combined = combined.cut(hole)

# Reinforcement rib on top of boss
rib = (
    cq.Workplane('XY')
    .workplane(offset=boss_height)
    .rect(rib_width, rib_length)
    .extrude(rib_thickness)
)
combined = combined.union(rib)

# Rectangular pocket on top of boss for weight reduction
pocket = (
    cq.Workplane('XY')
    .workplane(offset=boss_height + rib_thickness)
    .center(0, 0)
    .rect(pocket_width, pocket_depth)
    .extrude(-pocket_height)
)
combined = combined.cut(pocket)

# Fillet vertical edges
result = combined.edges("|Z").fillet(fillet_radius)
# Fillet edges on the top face
result = result.faces(">Z").edges().fillet(fillet_radius)
