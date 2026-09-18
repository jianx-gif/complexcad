import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    housing_width = 80.0,
    housing_depth = 50.0,
    housing_height = 20.0,
    wall_thickness = 4.0,
    cavity_depth_into = 30.0,
    cavity_width = 30.0,
    cavity_height = 12.0,
    internal_fillet = 2.0,
    outer_fillet = 2.0,
    latch_hole = Measures(
        offset = 20.0,
        diameter = 4.0,
        cbore_diameter = 6.5,
        cbore_depth = 3.0
    ),
    mounting_hole = Measures(
        positions = [(-30.0, -15.0), (30.0, -15.0)],
        diameter = 3.0,
        counterbore_diameter = 5.5,
        counterbore_depth = 2.5
    ),
    rib = Measures(
        width = 6.0,
        height = 8.0,
        length = 25.0,
        offset_from_front = 4.0 + 30.0 + 5.0  # wall + cavity + gap
    )
)

housing = (
    cq.Workplane("XY")
    .box(m.housing_width, m.housing_depth, m.housing_height)
    .translate((0.5 * m.housing_width, 0, 0.5 * m.housing_height))
    .edges(">Z").fillet(m.outer_fillet)
)

cavity = (
    cq.Workplane("XY")
    .rect(m.cavity_width, m.cavity_height)
    .extrude(m.cavity_depth_into)
    .translate((m.housing_width - m.wall_thickness - 0.5 * m.cavity_depth_into, 0, m.cavity_height / 2))
    .edges().fillet(m.internal_fillet)
)

housing = housing.cut(cavity)

rib = (
    cq.Workplane("XY")
    .box(m.rib.length, m.rib.width, m.rib.height)
    .translate((m.rib.offset_from_front + m.rib.length / 2, 0, m.rib.height / 2))
)

housing = housing.union(rib)

housing = (
    housing.faces(">X").workplane()
    .pushPoints([(-m.latch_hole.offset, 0), (m.latch_hole.offset, 0)])
    .cboreHole(m.latch_hole.diameter, m.latch_hole.cbore_diameter, m.latch_hole.cbore_depth)
)

housing = (
    housing.faces("<X").workplane()
    .pushPoints(m.mounting_hole.positions)
    .cboreHole(m.mounting_hole.diameter, m.mounting_hole.counterbore_diameter, m.mounting_hole.counterbore_depth)
)

result = housing