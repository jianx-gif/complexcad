import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    bushing_outer_radius = 20.0,
    bushing_inner_radius = 10.0,
    bushing_height = 30.0,
    flange_radius = 25.0,
    flange_height = 5.0,
    base_thickness = 2.0,
    central_hole_diameter = 8.0,
    set_screw_diameter = 4.0,
    set_screw_countersink_diameter = 8.0,
    set_screw_offset = 15.0,
    set_screw_depth = 4.0,
    fillet_radius = 1.0,
    pocket_depth = 2.0,
    pocket_clearance = 2.0,
)

profile = (
    cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(0, m.base_thickness)
    .lineTo(m.flange_radius, m.base_thickness)
    .lineTo(m.flange_radius, m.base_thickness + m.flange_height)
    .lineTo(m.bushing_outer_radius, m.base_thickness + m.flange_height)
    .lineTo(m.bushing_outer_radius, m.base_thickness + m.bushing_height)
    .lineTo(m.bushing_inner_radius, m.base_thickness + m.bushing_height)
    .lineTo(m.bushing_inner_radius, m.base_thickness)
    .close()
)

result = (
    profile
    .revolve()
    .edges('>Z')
    .fillet(m.fillet_radius)
    .faces('>Z')
    .workplane()
    .hole(m.central_hole_diameter)
    .workplane()
    .center(m.set_screw_offset, 0)
    .cskHole(m.set_screw_diameter, m.set_screw_countersink_diameter, m.set_screw_depth)
    .faces('>Z')
    .workplane(offset=-5)
    .circle(m.bushing_inner_radius - m.pocket_clearance)
    .cutBlind(-m.pocket_depth)
)
