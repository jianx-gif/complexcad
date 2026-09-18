import cadquery as cq
leaf_length = 80.0
leaf_width = 20.0
leaf_thickness = 5.0
tip_length = 10.0
groove_width = 4.0
groove_depth = 2.0
pin_hole_diameter = 3.0
fillet_radius = 1.0
rib_height = 2.0
rib_width = 6.0
rib_spacing = 12.0
path = cq.Workplane('XY').lineTo(leaf_length, 0).wire()
pts = [
    (0, -leaf_width/2),
    (0, leaf_width/2),
    (leaf_thickness, leaf_width/2),
    (leaf_thickness+tip_length, 0),
    (leaf_thickness, -leaf_width/2),
]
profile = cq.Workplane('YZ').polyline(pts).close()
leaf = profile.sweep(path, makeSolid=True, isFrenet=True)
rib_count = int((leaf_length - tip_length) // rib_spacing)
for i in range(rib_count):
    rib_x = (i+1) * rib_spacing
    rib = (
        cq.Workplane('XY')
        .center(rib_x, 0)
        .rect(rib_width, leaf_thickness)
        .extrude(rib_height)
        .translate((0, 0, -rib_height))
    )
    leaf = leaf.union(rib)

groove = (
    cq.Workplane('XY')
    .center(leaf_length/2, 0)
    .rect(groove_width, leaf_width)
    .extrude(groove_depth)
    .translate((0, 0, leaf_thickness - groove_depth))
)
leaf = leaf.cut(groove)
leaf = leaf.faces('>Z').workplane().hole(pin_hole_diameter)
leaf = leaf.edges().filter(lambda e: e.Center().x > leaf_length - 0.5).fillet(fillet_radius)
result = leaf