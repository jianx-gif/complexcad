import cadquery as cq
from math import sin, radians
from types import SimpleNamespace as NS

m = NS(
    chord_length=40.0,
    arc_angle_deg=60.0,
    profile_dia=12.0,
    thread_hole_dia=5.0,
    head_dia=9.0,
    head_depth=3.5,
    mounting_hole_dia=4.0,
    mounting_hole_offset=12.0,
    base_width=30.0,
    base_extra=10.0,
    side_cut_width=10.0,
    side_cut_depth=8.0,
    chamfer=1.0
)

m.arc_angle_rad = radians(m.arc_angle_deg)
m.arc_radius = m.chord_length / (2 * sin(m.arc_angle_rad / 2))

path = (
    cq.Workplane("XY")
    .radiusArc((m.chord_length, 0), m.arc_radius)
    .wire()
)

swept_body = (
    cq.Workplane("XY")
    .circle(m.profile_dia / 2)
    .sweep(path, transition="round")
)

base_plate = (
    cq.Workplane("XY")
    .rect(m.base_width, m.chord_length + m.base_extra)
    .extrude(m.profile_dia / 2)
)

combined = base_plate.union(swept_body)

# Add a side clearance pocket on the top face
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, - (m.base_extra / 2))
    .rect(m.side_cut_width, m.side_cut_depth)
    .cutBlind(-m.profile_dia / 2)
)

# Apply a small chamfer to outer vertical edges of the base
combined = (
    combined
    .edges("|Z")
    .chamfer(m.chamfer)
)

# Add functional holes on the top face
result = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cboreHole(m.thread_hole_dia, m.head_dia, m.head_depth)
    .pushPoints([
        (m.mounting_hole_offset, 0),
        (-m.mounting_hole_offset, 0)
    ])
    .cboreHole(m.mounting_hole_dia, m.head_dia, m.head_depth)
)
