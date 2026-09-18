import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    top_diameter = 80.0,
    top_height = 5.0,
    mid_height = 15.0,
    mid_diameter = 40.0,
    fillet_radius = 2.0,
    chamfer_distance = 1.5,
    vent_slot_width = 4.0,
    vent_slot_height = 12.0,
    vent_slot_depth = 20.0,
    vent_slot_count = 6,
    vent_slot_spacing = 30.0,
    vent_slot_count = 2,
    bowl_hole_dia = 5.0,
    screw_hole_spacing = 30.0,
    slot = (
        cq.Workplane('XZ')
        .lineTo(m.outer_diameter/2, 0)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2 + m.base_diameter, m.outer_diameter/2 + m.base_height)
        .lineTo(m.outer_diameter/2 + m.base_diameter, m.outer_diameter/2 + m.base_height)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2, m.outer_diameter/2)
        .lineTo(m.outer_diameter/2