import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Measures

# Parameters
m = Measures(
    linear_width=60.0,
    depth=20.0,
    height=12.0,
    arc_outer_diameter=95.0,
    top_fillet=3.0,
    vertical_fillet=2.0,
    chamfer=0.8,
    # T-slot dimensions
    tslot_head_width=30.0,
    tslot_head_height=8.0,
    tslot_head_depth=4.0,
    tslot_stem_width=12.0,
    tslot_stem_height=18.0,
    tslot_stem_depth=12.0,
    # Counterbore hole
    hole_x=20.0,
    hole_y=5.0,
    bolt_diameter=4.0,
    head_diameter=8.0,
    head_height=3.0
)

# Derived geometry
m.arc_outer_radius = 0.5 * m.arc_outer_diameter
m.arc_center_diameter = m.arc_outer_diameter - m.depth
m.arc_center_radius = 0.5 * m.arc_center_diameter
m.arc_center_angle = degrees(acos((2 * m.arc_center_radius**2 - m.linear_width**2) / (2 * m.arc_center_radius**2)))
m.arc_secant_angle = 0.5 * (180 - m.arc_center_angle)

# Path for sweep (arc edge)
path = (
    cq.Workplane("XY")
    .radiusArc((m.linear_width, 0.0), m.arc_center_radius)
    .wire()
)

# Base block creation by sweeping a rectangular section along the arc
base = (
    cq.Workplane("XY")
    .transformed(rotate=(90, -m.arc_secant_angle, 0))
    .rect(m.depth, m.height)
    .sweep(path, transition="round")
    .edges("|Z")
    .fillet(m.vertical_fillet)
    .edges(">Z")
    .fillet(m.top_fillet)
    .edges("<<Z")
    .chamfer(m.chamfer)
)

# Add T-slot on the top surface
with_tslot = (
    base.faces(">Z").workplane()
    .rect(m.tslot_head_width, m.tslot_head_height)
    .cutBlind(-m.tslot_head_depth)
    .rect(m.tslot_stem_width, m.tslot_stem_height)
    .cutBlind(-m.tslot_stem_depth)
)

# Counterbore hole placement
result = (
    with_tslot
    .faces(">Z").workplane()
    .center(m.hole_x, m.hole_y)
    .cboreHole(m.bolt_diameter, m.head_diameter, m.head_height)
)
