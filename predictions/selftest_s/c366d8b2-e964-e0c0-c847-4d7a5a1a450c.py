import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

# Parameters
m = Measures(
    linear_width=60.0,
    block_thickness=15.0,
    block_height=12.0,
    arc_outer_diameter=100.0,
    corner_fillet=2.0,
    vertical_fillet=1.5,
    hole_diameter=5.0,
    hole_spacing=20.0,
    hole_fillet=0.7,
    hole_rows=2,
    hole_columns=2,
)

# Derived dimensions
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
# Approximate inner radius for the sweep path so that the chord matches linear_width
# Using formula for radius of a circle given chord length (c) and sagitta (s): r = (c^2/(8*s)) + s
# Here sagitta = arc_outer_radius - block_thickness
m.sagitta = m.arc_outer_radius - m.block_thickness
m.arc_center_radius = (m.linear_width**2 / (8 * m.sagitta)) + m.sagitta
m.arc_center_angle = degrees(2 * acos(1 - (m.linear_width**2) / (2 * m.arc_center_radius**2)))
# Rotation to align rectangle normal to sweep path
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)

# Build the arc path (wire) for sweeping
arc_path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)

# Sweep a rectangular profile along the arc to form the curved block
swept = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.block_thickness, m.block_height)
    .sweep(arc_path, transition="round")
)

# Apply fillets to vertical edges and top edges for safety
base = (
    swept
    .edges("|Z")
    .fillet(m.vertical_fillet)
    .edges(">Z")
    .fillet(m.corner_fillet)
)

# Drill a patterned array of four through holes on the outer curved face (+X direction)
outer_face = base.faces(">X")
patterned = (
    outer_face.workplane()
    .rarray(m.hole_spacing, m.hole_spacing, m.hole_columns, m.hole_rows, center=True)
    .hole(m.hole_diameter)
)

# Fillet the entry edge of each hole (apply to all newly created circular edges)
result = (
    patterned
    .edges()
    .fillet(m.hole_fillet)
)
