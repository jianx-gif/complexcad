import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    outer_width = 60.0,
    outer_height = 30.0,
    thickness = 10.0,
    wall_thickness = 2.0,
    rib_width = 8.0,
    rib_height = 12.0,
    rib_thickness = 4.0,
    rib_count = 4,
    hole_diameter = 5.0,
    hole_offset_x = 20.0,
    hole_offset_y = 15.0,
    hole_diameter = 8.0,
    hole_offset_y = 20.0,
    hole_spacing = 20.0
)
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (m.outer_width, 0),
        (m.outer_width, m.outer_height),
        (m.outer_width, m.outer_height),
        (0, m.outer_height),
    ])
    .close()
    .extrude(m.thickness)
)
rib = (
    base.faces(">Z").workplane()
    .center(m.outer_width/2 - m.rib_width/2, m.outer_height/2)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
result = base.union(rib)
result = result.edges("|Z").chamfer(m.chamfer_size)
