import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    linear_width=50.0,
    depth=12.0,
    height=10.0,
    arc_outer_diameter=100.0,
    rib_width=20.0,
    rib_thickness=8.0,
    rib_height=5.0,
    tap_diameter=4.2,
    tap_depth=8.0,
    chamfer_distance=0.8,
)
base = (
    cq.Workplane("XY")
    .sketch()
    .rect(m.depth, m.depth)
    .sweep(path, transition="round")
)
base = base.edges("|Z").chamfer(m.chamfer_distance)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(m.depth - 2 * m.depth, m.depth - 2 * m.depth)
    .extrude(m.height)
)
base = base.edges("|Z").chamfer(m.chamfer_distance)
base = (
    base.faces(">Z").workplane()
    .center(m.depth/2, 0)
    .rect(m.depth - 2 * m.depth, m.depth - 2 * m.depth)
    .extrude(m.height)
)
base = base.edges("|Z").chamfer(m.chamfer_distance)
result = base
