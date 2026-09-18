import cadquery as cq

# Parameters
outer_diameter = 80.0
inner_diameter = 60.0
height = 20.0
rim_thickness = 5.0
fillet_radius = 2.0
# Groove parameters
groove_width = 3.0
groove_depth = 2.0
# Derived values
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
# Groove radii
groove_center_radius = outer_radius - rim_thickness / 2.0
groove_outer_radius = groove_center_radius + groove_width / 2.0
groove_inner_radius = groove_center_radius - groove_width / 2.0

def base_cover(inner_r, outer_r, total_h, rim_t):
    profile = (
        cq.Workplane("XY")
        .moveTo(inner_r, 0)
        .lineTo(inner_r, total_h - rim_t)
        .lineTo(outer_r, total_h - rim_t)
        .lineTo(outer_r, total_h)
        .lineTo(inner_r, total_h)
        .close()
    )
    return profile.revolve()

cover = base_cover(inner_radius, outer_radius, height, rim_thickness)
# Fillet the inner top rim edge (circular edge on the top face)
cover = cover.edges(">Z and %Circle").fillet(fillet_radius)
# Create annular groove as a thin ring and cut it from the cover
outer_cyl = (
    cq.Workplane("XY")
    .circle(groove_outer_radius)
    .extrude(groove_depth)
    .translate((0, 0, height - groove_depth))
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(groove_inner_radius)
    .extrude(groove_depth)
    .translate((0, 0, height - groove_depth))
)
groove_ring = outer_cyl.cut(inner_cyl)
result = cover.cut(groove_ring)
