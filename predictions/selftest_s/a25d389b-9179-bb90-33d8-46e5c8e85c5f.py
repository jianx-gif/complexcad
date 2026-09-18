import cadquery as cq

# Parameters
outer_diameter = 80.0
body_length = 70.0
wall_thickness = 5.0
bore_diameter = 40.0
lip_height = 8.0
lip_thickness = 2.0
lip_gap = 1.0
vent_slot_width = 5.0
vent_slot_height = 30.0
chamfer_size = 0.5

# Derived dimensions
outer_radius = outer_diameter / 2.0
bore_radius = bore_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Base hollow cylinder
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(body_length)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(body_length)
body = outer_cyl.cut(inner_cyl)

# Helper to create annular cut (ring) at given Z center
def annular_cut(z_center):
    return (
        cq.Workplane('XY')
        .circle(bore_radius + lip_thickness)
        .circle(bore_radius)
        .extrude(lip_height)
        .translate((0, 0, z_center))
    )

# Top double‑lip cuts
top_first_z = body_length/2 - lip_height/2
top_second_z = body_length/2 - lip_height - lip_gap - lip_height/2
# Bottom double‑lip cuts
bottom_first_z = -(body_length/2) + lip_height/2
bottom_second_z = -(body_length/2) + lip_height + lip_gap + lip_height/2

cuts = (
    annular_cut(top_first_z)
    .union(annular_cut(top_second_z))
    .union(annular_cut(bottom_first_z))
    .union(annular_cut(bottom_second_z))
)

result = body.cut(cuts)

# Venting slot cut using a rectangular prism positioned on outer wall
vent_slot = (
    cq.Workplane('XY')
    .box(wall_thickness + 0.2, vent_slot_width, vent_slot_height)
    .translate((outer_radius - (wall_thickness + 0.2)/2, 0, 0))
)
result = result.cut(vent_slot)

# Chamfer all edges for safety
result = result.edges().chamfer(chamfer_size)
