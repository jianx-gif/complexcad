import cadquery as cq
from types import SimpleNamespace as Measures

params = Measures(
    inner_radius=30.0,
    wall_thickness=5.0,
    cup_height=70.0,
    flange_height=10.0,
    flange_extra=10.0,
    lip_height=5.0,
    fillet_radius=3.0,
    hole=Measures(
        diameter=8.0,
        counterbore_diameter=12.0,
        counterbore_depth=5.0,
        pattern_radius=45.0,
        count=3
    ),
    pocket=Measures(
        width=15.0,
        height=10.0,
        depth=8.0,
        offset=20.0
    )
)

p = params

profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(p.inner_radius, 0)
    .lineTo(p.inner_radius, p.cup_height)
    .lineTo(p.inner_radius + p.wall_thickness, p.cup_height)
    .lineTo(p.inner_radius + p.wall_thickness, p.cup_height + p.flange_height)
    .lineTo(p.inner_radius + p.wall_thickness + p.flange_extra, p.cup_height + p.flange_height)
    .lineTo(p.inner_radius + p.wall_thickness + p.flange_extra, p.cup_height + p.flange_height + p.lip_height)
    .lineTo(0, p.cup_height + p.flange_height + p.lip_height)
    .close()
)

cup = profile.revolve()

cup = cup.faces(">Z").edges().fillet(p.fillet_radius)

cup = (
    cup.faces(">Z")
    .workplane()
    .polarArray(radius=p.hole.pattern_radius, startAngle=0, count=p.hole.count, angle=360)
    .cboreHole(p.hole.diameter, p.hole.counterbore_diameter, p.hole.counterbore_depth)
)

cup = (
    cup.faces(">X")
    .workplane()
    .center(p.pocket.offset, 0)
    .rect(p.pocket.width, p.pocket.height)
    .cutBlind(p.pocket.depth)
)

result = cup