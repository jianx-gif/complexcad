import cadquery as cq

class Measures:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

params = Measures(
    brace_thickness=5.0,
    leg_width=20.0,
    leg_long=80.0,
    leg_short=50.0,
    slot_width=12.0,
    slot_offset=30.0,
    hole_diameter=8.0,
    hole_offset_x=15.0,
    hole_offset_y=10.0,
    perforation_diameter=3.0,
    perforation_spacing=15.0,
    fillet_radius=1.0,
)

p = params

def l_profile():
    pts = [
        (0, 0),
        (p.leg_long, 0),
        (p.leg_long, p.leg_width),
        (p.leg_width, p.leg_width),
        (p.leg_width, p.leg_short),
        (0, p.leg_short),
        (0, 0),
    ]
    return cq.Workplane("XY").polyline(pts).close()

base = l_profile().extrude(p.brace_thickness)
base = base.edges().fillet(p.fillet_radius)

slot_center_x = p.leg_long - p.slot_offset
slot = (
    base
    .faces(">Z")
    .workplane()
    .center(slot_center_x - p.leg_long/2, p.leg_width/2)
    .rect(p.slot_width, p.leg_width)
    .cutBlind(-p.brace_thickness)
)

hole = (
    slot
    .faces(">Z")
    .workplane()
    .center(p.hole_offset_x - p.leg_long/2, p.hole_offset_y - p.leg_short/2)
    .hole(p.hole_diameter)
)

nx = int(p.leg_long / p.perforation_spacing) + 1
ny = int(p.leg_short / p.perforation_spacing) + 1
points = []
for i in range(nx):
    for j in range(ny):
        x = -p.leg_long/2 + i * p.perforation_spacing
        y = -p.leg_short/2 + j * p.perforation_spacing
        points.append((x, y))

result = (
    hole
    .faces(">Z")
    .workplane()
    .pushPoints(points)
    .hole(p.perforation_diameter)
)
