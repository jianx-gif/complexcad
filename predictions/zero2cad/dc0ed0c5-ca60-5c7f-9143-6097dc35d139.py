import cadquery as cq

# Parameters
total_length = 80.0
inlet_radius = 10.0
outlet_radius = 25.0
wall_thickness = 1.5
fillet_radius = 2.0
vent_hole_diameter = 2.5
vent_rows = 4
vent_cols = 6
vent_spacing = 6.0

# Build outer lofted shape
outer = (
    cq.Workplane("XY")
    .circle(inlet_radius)
    .workplane(offset=total_length)
    .circle(outlet_radius)
    .loft(combine=True)
)

# Fillet all edges for safety
outer = outer.edges().fillet(fillet_radius)

# Shell to create thin wall
hollow = outer.shell(-wall_thickness)

# Add vent holes on the outlet face
result = (
    hollow
    .faces(">Z")
    .workplane()
    .rarray(vent_spacing, vent_spacing, vent_cols, vent_rows)
    .hole(vent_hole_diameter)
)
