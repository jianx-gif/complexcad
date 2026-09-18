import cadquery as cq
import math
from types import SimpleNamespace as Measures

m = Measures(
    outer_diameter = 40.0,
    inner_diameter_top = 20.0,
    taper_angle = 10.0,
    spacer_height = 30.0,
    top_thickness = 4.0,
    bottom_fillet_radius = 2.0,
    top_hole_dia = 3.0,
    top_hole_spacing = 25.0,
    wall_thickness_min = 2.0
)

outer_radius = m.outer_diameter/2.0
inner_radius_top = m.inner_diameter_top/2.0
taper_rad = math.radians(m.taper_angle)
inner_radius_bottom = inner_radius_top - m.spacer_height * math.tan(taper_rad)
if inner_radius_bottom < m.wall_thickness_min:
    inner_radius_bottom = m.wall_thickness_min

profile = (
    cq.Workplane('XZ')
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, m.spacer_height - m.top_thickness)
    .lineTo(outer_radius, m.spacer_height)
    .lineTo(inner_radius_top, m.spacer_height)
    .lineTo(inner_radius_bottom, 0)
    .lineTo(outer_radius, 0)
    .close()
)

result = (
    profile
    .revolve()
    .edges()
    .fillet(m.bottom_fillet_radius)
    .faces('>Z')
    .workplane()
    .pushPoints([
        ( m.top_hole_spacing/2,  m.top_hole_spacing/2),
        (-m.top_hole_spacing/2,  m.top_hole_spacing/2),
        (-m.top_hole_spacing/2, -m.top_hole_spacing/2),
        ( m.top_hole_spacing/2, -m.top_hole_spacing/2)
    ])
    .hole(m.top_hole_dia)
)