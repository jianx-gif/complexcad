import cadquery as cq

# Parameters
leg_length = 80.0
leg_width = 60.0
leg_thickness = 8.0
wall_thickness = 1.5
extrude_depth = 30.0
outer_fillet = 1.0
chamfer_dist = 0.3
hole_diameter = 4.0
hole_spacing = 15.0
holes_per_leg = 3

# Composite L profile (non‑trivial closed sketch)
profile = (
    cq.Workplane("XY")
    .lineTo(leg_width, 0)
    .lineTo(leg_width, leg_thickness)
    .lineTo(leg_thickness, leg_thickness)
    .lineTo(leg_thickness, leg_length)
    .lineTo(0, leg_length)
    .close()
)

# Create thin‑walled channel with chamfer before fillet
result = (
    profile
    .extrude(extrude_depth)
    .shell(-wall_thickness)
    .edges("|X")
    .chamfer(chamfer_dist)
    .edges("|Z")
    .fillet(outer_fillet)
)

# Offsets for hole patterns
inner_vert_height = leg_length - 2 * wall_thickness
vert_start = (inner_vert_height - (holes_per_leg - 1) * hole_spacing) / 2
inner_horiz_width = leg_width - 2 * wall_thickness
horiz_start = (inner_horiz_width - (holes_per_leg - 1) * hole_spacing) / 2

# Holes on inner vertical face
result = (
    result
    .faces(">X")
    .workplane()
    .center(0, vert_start)
    .rarray(0, hole_spacing, 1, holes_per_leg)
    .hole(hole_diameter)
)

# Holes on inner horizontal face
result = (
    result
    .faces("<Y")
    .workplane()
    .center(horiz_start, 0)
    .rarray(hole_spacing, 0, holes_per_leg, 1)
    .hole(hole_diameter)
)
