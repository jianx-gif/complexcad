import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 50.0
plate_thickness = 10.0
central_dome_radius = 12.0
central_dome_height = 5.0
groove_width = 4.0
groove_depth = 2.0
countersink_top_diameter = 8.0
countersink_angle = 90.0
countersink_bottom_diameter = 6.0
hole_pattern_radius = (inner_diameter/2 + outer_diameter/2) / 2
rib_width = 4.0
rib_height = 3.0
rib_spacing = 20.0
edge_chamfer = 1.0
inner_fillet = 0.8

base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(plate_thickness)
)

central_dome = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(central_dome_radius)
    .extrude(central_dome_height)
    .edges(">Z")
    .fillet(central_dome_height / 2)
)

groove_cut = (
    cq.Workplane("XY")
    .circle((outer_diameter - groove_width) / 2)
    .circle(outer_diameter / 2)
    .extrude(groove_depth)
    .translate((0, 0, plate_thickness - groove_depth))
)

countersink_bottom_radius = countersink_bottom_diameter / 2
countersink_top_radius = countersink_top_diameter / 2
cone_height = (countersink_top_radius - countersink_bottom_radius) / math.tan(math.radians(countersink_angle / 2))

def make_countersink(x, y):
    wp = cq.Workplane("XY").center(x, y)
    cylinder = wp.circle(countersink_bottom_radius).extrude(plate_thickness)
    cone = cq.Solid.makeCone(countersink_bottom_radius, countersink_top_radius, cone_height)
    cone = cone.translate((x, y, plate_thickness))
    return cylinder.union(cone)

central_cut = make_countersink(0, 0)
peripheral_cuts = []
for i in range(6):
    angle = math.radians(i * 60)
    x = hole_pattern_radius * math.cos(angle)
    y = hole_pattern_radius * math.sin(angle)
    peripheral_cuts.append(make_countersink(x, y))

all_hole_cuts = central_cut
for cut in peripheral_cuts:
    all_hole_cuts = all_hole_cuts.union(cut)

core = (
    base
    .cut(groove_cut)
    .union(central_dome)
    .cut(all_hole_cuts)
    .edges(">Z")
    .chamfer(edge_chamfer)
    .edges("<Z")
    .fillet(inner_fillet)
)

ribs = []
limit = outer_diameter / 2 - rib_width
for x in range(-int(limit), int(limit) + 1, int(rib_spacing)):
    for y in range(-int(limit), int(limit) + 1, int(rib_spacing)):
        if (x**2 + y**2) < (limit**2):
            rib = (
                cq.Workplane("XY")
                .center(x, y)
                .rect(rib_width, rib_width)
                .extrude(rib_height)
            )
            ribs.append(rib)

rib_union = None
for r in ribs:
    rib_union = r if rib_union is None else rib_union.union(r)

result = core.union(rib_union)
