import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=80.0,
    depth=50.0,
    thickness=10.0,
    arc_outer_diameter=12.0,
    rib_width=4.0,
    rib_height=3.0,
    rib_thickness=2.0,
    rib_spacing=12.0,
    hole_diameter=5.0,
    hole_spacing=15.0,
    hole_offset_x=20.0
)
base = (
    cq.Workplane("XY")
    .rect(m.width, m.depth)
    .extrude(m.thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.rib_width, m.rib_height)
    .extrude(m.rib_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.rib_width, m.depth)
    .extrude(m.rib_thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(m.rib_width, m.depth)
    .extrude(m.rib_thickness)
)
result = base.union(base)
