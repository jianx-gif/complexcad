import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    outer_radius=30.0,
    inner_radius=20.0,
    height=35.0,
    top_fillet=2.0,
    central_hole_diameter=6.0,
    slot_width=4.0,
    slot_height=10.0,
    slot_depth=5.0,
    slot_center_z=17.5,
)

profile = (
    cq.Workplane("XZ")
    .moveTo(m.inner_radius, 0)
    .lineTo(m.inner_radius, m.height - m.top_fillet)
    .threePointArc((m.inner_radius + (m.outer_radius - m.inner_radius) / 2, m.height), (m.outer_radius, m.height - m.top_fillet))
    .lineTo(m.outer_radius, 0)
    .close()
)

solid = profile.revolve()

solid = solid.faces(">Z").hole(m.central_hole_diameter)

slot = (
    cq.Workplane("XY")
    .box(m.slot_depth, m.slot_width, m.slot_height)
    .translate((m.outer_radius - m.slot_depth / 2, 0, m.slot_center_z))
)

result = solid.cut(slot)
