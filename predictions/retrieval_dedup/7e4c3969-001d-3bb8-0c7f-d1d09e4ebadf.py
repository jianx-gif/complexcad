import cadquery as cq

inner_diam = 10.1
inner_radius = inner_diam / 2.0
outer_diam = 15.0
outer_radius = outer_diam / 2.0
height = 2.0
chamfer = 0.06
hole_dia = 1.9
counterbore_dia = 3.5
counterbore_depth = 0.5
tab_width = 3.0
tab_height = 1.0
tab_depth = 1.0
pocket_width = 4.0
pocket_depth = 1.5
pocket_height = 0.8

outer_cyl = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(height)
)
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(height)
)
base = outer_cyl.cut(inner_cyl)

# Tab overlaps cylinder by half its depth for proper fusion
tab = (
    cq.Workplane("XY")
    .box(tab_depth, tab_width, tab_height)
    .translate((outer_radius - tab_depth/2.0, 0, height/2.0))
)

pocket = (
    cq.Workplane("XY")
    .box(pocket_depth, pocket_width, pocket_height)
    .translate((outer_radius - pocket_depth/2.0, 0, height/2.0))
)

through_hole = (
    cq.Workplane("XY")
    .circle(hole_dia/2.0)
    .extrude(height + 1.0)
)

counterbore = (
    cq.Workplane("XY")
    .circle(counterbore_dia/2.0)
    .extrude(counterbore_depth)
    .translate((0, 0, height - counterbore_depth))
)

result = base.union(tab)
result = result.cut(pocket)
result = result.cut(through_hole)
result = result.cut(counterbore)
result = result.edges("|Z").chamfer(chamfer)
