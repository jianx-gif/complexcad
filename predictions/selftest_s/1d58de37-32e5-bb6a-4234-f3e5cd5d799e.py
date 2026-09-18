import cadquery as cq
from types import SimpleNamespace as Params

p = Params(
    total_width=70.0,
    leg_height=30.0,
    bar_depth=10.0,
    spacer_thickness=5.0,
    leg_thickness=8.0,
    boss_radius=12.0,
    boss_height=8.0,
    chamfer=0.8,
    hole_dia=4.0,
    hole_spacing=30.0,
)

bar_width = p.total_width - 2 * p.leg_thickness

# Z‑profile extruded solid
z_body = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (0, p.leg_height),
        (p.leg_thickness, p.leg_height),
        (p.leg_thickness, p.leg_height + p.bar_depth),
        (p.leg_thickness + bar_width, p.leg_height + p.bar_depth),
        (p.leg_thickness + bar_width, p.leg_height),
        (p.total_width, p.leg_height),
        (p.total_width, 0),
        (0, 0),
    ])
    .close()
    .extrude(p.spacer_thickness)
)

# Side‑mounted cylindrical boss (oriented along X)
boss = (
    cq.Workplane("YZ")
    .center(p.leg_height + p.bar_depth/2, p.spacer_thickness/2)
    .circle(p.boss_radius)
    .extrude(p.boss_height)
    .translate((p.total_width, 0, 0))
)

with_boss = z_body.union(boss)

# Through‑hole pattern on the top face of the horizontal bar region
hole_plane = (
    with_boss
    .faces(">Z")
    .workplane()
    .center(p.total_width/2, p.leg_height + p.bar_depth/2)
)

hole_pattern = (
    hole_plane
    .rarray(p.hole_spacing, 0, 1, 1)
    .hole(p.hole_dia)
)

# Apply chamfer to all outer edges
result = (
    hole_pattern
    .edges()
    .chamfer(p.chamfer)
)
