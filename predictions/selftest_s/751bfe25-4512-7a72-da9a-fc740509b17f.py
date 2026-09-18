import cadquery as cq
from types import SimpleNamespace as Measures

m = Measures(
    disc_diameter=80.0,
    disc_thickness=5.0,
    rim_radial_thickness=5.0,
    rim_height=4.0,
    boss_diameter=20.0,
    boss_height=3.0,
    chamfer=0.5,
    hole=Measures(
        diameter=5.0,
        countersink_diameter=8.5,
        countersink_depth=2.0,
        count=4,
        radius_offset=0.0
    )
)

inner_radius = m.disc_diameter / 2.0
outer_radius = inner_radius + m.rim_radial_thickness

base = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(m.disc_thickness)
)

rim_profile = (
    cq.Workplane("XZ")
    .transformed(offset=(0, 0, m.disc_thickness))
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .radiusArc((outer_radius, m.rim_height), radius=m.rim_height)
    .lineTo(inner_radius, m.rim_height)
    .close()
    .revolve()
)

boss = (
    cq.Workplane("XY")
    .circle(m.boss_diameter / 2.0)
    .extrude(m.boss_height)
    .translate((0, 0, m.disc_thickness))
)

result = base.union(rim_profile).union(boss)

result = result.edges("|Z").chamfer(m.chamfer)

hole_center_radius = inner_radius + m.rim_radial_thickness / 2.0

result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=hole_center_radius, count=m.hole.count, startAngle=0, angle=360)
    .cboreHole(m.hole.diameter, m.hole.countersink_diameter, m.hole.countersink_depth)
)
