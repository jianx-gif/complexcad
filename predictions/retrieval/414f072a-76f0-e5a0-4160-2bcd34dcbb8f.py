import cadquery as cq
import math

housing_outer_radius = 30
housing_inner_radius = 22
housing_length = 60
wall_thickness = housing_outer_radius - housing_inner_radius
boss_radius = 12
boss_depth = 15
through_hole_diameter = 12
mounting_hole_diameter = 6
mounting_hole_circle_radius = 22
chamfer_distance = 1
slot_width = 8
slot_length = 30
slot_depth = 5
rib_thickness = 4
rib_length = 30
rib_height = 6
countersink_diameter = 8
countersink_depth = 2

outer_cyl = cq.Workplane("XY").circle(housing_outer_radius).extrude(housing_length)

boss_pocket = (
    cq.Workplane("XY")
    .center(0, housing_outer_radius - boss_radius)
    .circle(boss_radius)
    .extrude(-boss_depth)
)
outer_cyl = outer_cyl.cut(boss_pocket)

inner_cyl = cq.Workplane("XY").circle(housing_inner_radius).extrude(housing_length)
base = outer_cyl.cut(inner_cyl)

base = base.faces(">Z").workplane().hole(through_hole_diameter)

boss_protrusion = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_depth)
    .translate((housing_inner_radius - boss_radius, 0, housing_length/2))
)
base = base.union(boss_protrusion)

rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_length, rib_height)
    .translate((housing_inner_radius - rib_thickness/2, 0, housing_length/2))
)
base = base.union(rib)

mounting_cuts = cq.Workplane("XY")
for angle in [0, 90, 180, 270]:
    x = mounting_hole_circle_radius * math.cos(math.radians(angle))
    y = mounting_hole_circle_radius * math.sin(math.radians(angle))
    hole_cyl = (
        cq.Workplane("YZ")
        .circle(mounting_hole_diameter/2)
        .extrude(wall_thickness*2)
        .translate((x, y, housing_length/2))
    )
    mounting_cuts = mounting_cuts.union(hole_cyl)
base = base.cut(mounting_cuts)

base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(-slot_depth)
)

base = (
    base
    .faces("<Z")
    .workplane()
    .center(0, 0)
    .rect(slot_width, slot_length)
    .cutBlind(slot_depth)
)

base = (
    base
    .faces(">Z")
    .workplane()
    .hole(countersink_diameter, depth=countersink_depth)
)

result = base.edges("|Z").chamfer(chamfer_distance)
