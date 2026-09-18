import cadquery as cq

# Parameters
leg_length = 80.0
leg_width = 20.0
thickness = 8.0
fillet_radius = 3.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_offset = 10.0
pocket_width = 12.0
pocket_depth = 4.0
pocket_offset = 5.0

# Base L‑shape profile
profile = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (leg_length, 0),
        (leg_length, leg_width),
        (leg_width, leg_width),
        (leg_width, leg_length),
        (0, leg_length),
        (0, 0),
    ])
    .close()
)

# Extrude to thickness
result = profile.extrude(thickness)

# Fillet inner corner (vertical edge at inner corner)
inner_corner_edge = (
    result.edges()
    .filter(lambda e: abs(e.Center().x - leg_width) < 1e-3 and abs(e.Center().y - leg_width) < 1e-3)
)
result = inner_corner_edge.fillet(fillet_radius)

# Chamfer outer edges for safety
outer_edges = (
    result.edges()
    .filter(
        lambda e: (
            abs(e.Center().x) < 1e-3 or abs(e.Center().x - leg_length) < 1e-3 or
            abs(e.Center().y) < 1e-3 or abs(e.Center().y - leg_length) < 1e-3
        )
    )
)
result = outer_edges.chamfer(chamfer_distance)

# Add a rectangular pocket on the horizontal leg for weight reduction
pocket = (
    cq.Workplane("XY")
    .center(leg_length/2, leg_width/2)
    .rect(pocket_width, pocket_depth)
    .extrude(-thickness)
)
result = result.cut(pocket)

# Drill five through holes on the vertical leg (face with normal +Y)
vertical_face = result.faces(">Y")
vertical_wp = vertical_face.workplane()
vertical_wp = vertical_wp.center(leg_width/2, hole_offset)
vertical_wp = vertical_wp.rarray(0, hole_spacing, 1, 5)
result = vertical_wp.hole(hole_diameter)
