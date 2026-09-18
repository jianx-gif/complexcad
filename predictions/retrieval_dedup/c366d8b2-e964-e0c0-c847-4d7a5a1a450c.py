import cadquery as cq
from math import acos, degrees
from types import SimpleNamespace as Ns

# Parameters
p = Ns(
    linear_width=55.0,
    depth=12.0,
    height=10.0,
    arc_outer_diameter=90.0,
    chamfer_distance=1.0,
    vertical_fillet=1.5,
    top_fillet=1.0,
    pocket_radius=3.0,
    pocket_offset_x=20.0,
    pocket_offset_y=5.0,
    keyhole_circle_radius=2.5,
    keyhole_slot_length=8.0,
    keyhole_offset_x=35.0,
    keyhole_offset_y=5.0
)

# Derived dimensions
p.arc_outer_radius = 0.5 * p.arc_outer_diameter
p.arc_center_radius = p.arc_outer_radius - p.depth
p.arc_center_angle = degrees(
    acos((2 * p.arc_center_radius ** 2 - p.linear_width ** 2) / (2 * p.arc_center_radius ** 2))
)
p.arc_secant_angle = 0.5 * (180.0 - p.arc_center_angle)

# Build the sweep path (arc)
arc_path = (
    cq.Workplane("XY")
    .radiusArc((p.linear_width, 0.0), p.arc_center_radius)
    .wire()
)

# Sweep a rectangle along the arc to create the block and add features
result = (
    cq.Workplane("XY")
    .transformed(rotate=(90.0, -p.arc_secant_angle, 0.0))
    .rect(p.depth, p.height)
    .sweep(arc_path, transition="round")
    .edges("|Z")
    .fillet(p.vertical_fillet)
    .edges(">Z")
    .fillet(p.top_fillet)
    # Pocket on side face
    .faces(">Y")
    .workplane()
    .center(p.pocket_offset_x, p.pocket_offset_y)
    .circle(p.pocket_radius)
    .cutBlind(-p.depth)
    # Keyhole slot on same side face
    .center(p.keyhole_offset_x - p.pocket_offset_x, p.keyhole_offset_y - p.pocket_offset_y)
    .circle(p.keyhole_circle_radius)
    .cutBlind(-p.depth)
    .center(0, -p.keyhole_circle_radius)
    .rect(p.keyhole_slot_length, 2 * p.keyhole_circle_radius)
    .cutBlind(-p.depth)
    # Chamfer entry edge (leading edge of block)
    .edges("<X")
    .chamfer(p.chamfer_distance)
)
