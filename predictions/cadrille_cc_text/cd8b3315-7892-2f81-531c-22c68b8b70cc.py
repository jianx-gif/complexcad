import cadquery as cq
spacer_length = 80.0
spacer_width = 50.0
spacer_height = 12.0
wall_thickness = 4.0
rib_thickness = 2.0
rib_spacing = 15.0
tab_width = 10.0
tab_height = 5.0
chamfer_distance = 0.8
interior_width = spacer_width - 2 * wall_thickness
interior_height = spacer_height - 2 * wall_thickness
tab_length = 30.0
tab_width = 10.0
tab_height = 5.0
base = cq.Workplane('XY').box(spacer_length, spacer_width, spacer_height)
rib = (
    cq.Workplane('XY')
    .box(spacer_length, rib_thickness, rib_spacing)
    .translate((0, 0, rib_spacing))
)
interior = (
    cq.Workplane('XY')
    .box(interior_width, rib_thickness, rib_spacing)
    .translate((0, 0, spacer_height))
)
interior = (
    cq.Workplane('XY')
    .box(interior_width, rib_thickness, rib_spacing)
    .translate((0, 0, spacer_height))
)
interior = (
    cq.Workplane('XY')
    .box(interior_width, spacer_width, rib_spacing)
    .translate((0, 0, spacer_height))
)
interior = (
    cq.Workplane('XY')
    .box(interior_width, spacer_width, rib_thickness)
    .translate((0, 0, spacer_height))
)
interior = (
    cq.Workplane('XY')
    .box(interior_width, spacer_width, rib_thickness)
    .translate((0, 0, spacer_height))
)
interior = (
    cq.Workplane('XY')
    .box(interior_width, spacer_width, rib_thickness)
    .translate((0, 0, spacer_height))
)
interior = (
    cq.Workplane('XY')
    .box(interior_width, spacer_width, rib_thickness)
    .translate((0, 0, spacer_height))
)
interior = (
    cq.Workplane('XY')
    .box(interior_width, spacer_width, rib_thickness)
    .translate((0, 0, spacer_height))
)
result = inter.union(interior)
