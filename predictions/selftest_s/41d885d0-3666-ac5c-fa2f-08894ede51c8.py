import cadquery as cq
from types import SimpleNamespace as Measures

measures = Measures(
    plate_width=80.0,
    plate_depth=50.0,
    plate_thickness=5.0,
    edge_fillet=2.0,
    chamfer=0.5,
    aperture_width=30.0,
    aperture_height=10.0,
    stud_diameter=6.0,
    stud_height=4.0,
    hole=Measures(
        diameter=2.5,
        cbore_diameter=5.0,
        cbore_depth=2.0
    ),
    stud_positions=[
        (20.0, -20.0),
        (0.0, -20.0),
        (-20.0, -20.0)
    ]
)

m = measures

base = (
    cq.Workplane('XY')
    .box(m.plate_width, m.plate_depth, m.plate_thickness)
    .translate((0.5 * m.plate_width, 0, 0.5 * m.plate_thickness))
    .edges('>Z').fillet(m.edge_fillet)
    .edges('<<Z or >>Z').chamfer(m.chamfer)
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .ellipse(m.aperture_width, m.aperture_height)
    .cutBlind(-m.plate_thickness)
)

studs = (
    cq.Workplane('XY')
    .workplane()
    .pushPoints(m.stud_positions)
    .circle(m.stud_diameter / 2)
    .extrude(m.stud_height)
    .translate((0.5 * m.plate_width, 0, m.plate_thickness))
)

result = base.union(studs)

result = (
    result
    .faces('>Z')
    .workplane()
    .pushPoints(m.stud_positions)
    .cboreHole(m.hole.diameter, m.hole.cbore_diameter, m.hole.cbore_depth)
)
