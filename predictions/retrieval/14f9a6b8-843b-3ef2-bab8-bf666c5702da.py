import cadquery as cq
from types import SimpleNamespace as Measures

params = Measures(
    base_diameter = 40.0,
    base_height = 10.0,
    key_thickness = 12.0,
    key_height = 20.0,
    slot_width_top = 4.0,
    slot_width_bottom = 8.0,
    slot_length = 12.0,
    central_hole_dia = 6.0,
    mounting_hole_dia = 3.0,
    mounting_hole_offset = 15.0,
    fillet_radius = 0.5,
)

p = params

base = (
    cq.Workplane('XY')
    .circle(p.base_diameter / 2)
    .extrude(p.base_height)
)

key_profile = (
    cq.Workplane('XZ')
    .center(p.base_diameter / 2, 0)
    .lineTo(p.base_diameter / 2 + p.key_thickness, 0)
    .vLine(p.key_height)
    .lineTo(p.base_diameter / 2 + p.slot_width_bottom / 2, p.key_height - p.slot_length)
    .lineTo(p.base_diameter / 2 + p.slot_width_top / 2, p.key_height)
    .lineTo(p.base_diameter / 2, p.key_height)
    .close()
)
key = key_profile.revolve().translate((0, 0, p.base_height))

slot_profile = (
    cq.Workplane('XZ')
    .center(p.base_diameter / 2 + p.slot_width_bottom / 2, p.key_height - p.slot_length)
    .rect(p.slot_width_bottom, p.slot_length)
)
slot = slot_profile.extrude(p.key_thickness + 2).translate((0, 0, p.base_height))

central_hole = (
    cq.Workplane('XY')
    .circle(p.central_hole_dia / 2)
    .extrude(p.base_height + p.key_height)
)

mounting_holes = (
    cq.Workplane('XY')
    .pushPoints([
        (p.mounting_hole_offset, 0),
        (-p.mounting_hole_offset, 0),
        (0, p.mounting_hole_offset),
        (0, -p.mounting_hole_offset)
    ])
    .circle(p.mounting_hole_dia / 2)
    .extrude(p.base_height + p.key_height)
)

result = (
    base.union(key)
    .cut(slot)
    .cut(central_hole)
    .cut(mounting_holes)
    .edges("|Z")
    .fillet(p.fillet_radius)
)
