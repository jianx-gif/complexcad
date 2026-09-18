import cadquery as cq
from types import SimpleNamespace as Measures
m = Measures(
    width=60.0,
    depth=40.0,
    thickness=8.0,
    wall=2.0,
    chamfer=0.5,
    hole_diameter=4.0,
    hole_spacing=30.0,
    top_radius=2.0,
    relief_thickness=6.0,
    relief_depth=30.0,
    hole_diameter=4.0,
    hole_spacing=30.0,
)
base = (
    cq.Workplane("XY")
    .rect(m.width, m.depth)
    .extrude(m.thickness)
)
base = base.edges("|Z").fillet(m.top_radius)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(m.relance_thickness, m.relance_thickness)
    .cutBlind(-m.thickness)
)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(m.rib_thickness, m.rib_height)
    .extrude(m.rib_thickness)
)
base = base.union(rib)
base = (
    base.faces(">Z").workplane()
    .center(-m.hole_spacing/2, 0)
    .hole(m.hole_diameter)
)
base = (
    base.faces(">Z").workplane()
    .center(m.hole_spacing, 0)
    .hole(m.hole_diameter)
)
base = (
    base.faces(">Z").workplane()
    .center(m.hole_spacing, 0)
    .hole(m.hole_diameter)
)
result = base
