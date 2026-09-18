import cadquery as cq
base_width = 80.0
base_height = 60.0
thickness = 8.0
tab_width = 40.0
tab_height = 30.0
cut_angle = 45.0
edge_chamfer = 1.0
pocket_width = 20.0
pocket_length = 30.0
pocket_depth = 6.0
screw_hole_dia = 4.0
screw_head_dia = 7.0
screw_head_dia = 2.0
screw_spacing = 25.0
screw_offset = base_height / 2.0
screw_offset = base_width / 2.0
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(thickness)
)
tab = (
    cq.Workplane("XY")
    .rect(tab_width, tab_height)
    .translate((0, 0, thickness))
)
tab = (
    cq.Workplane("XY")
    .rect(tab_width, tab_height)
    .translate((0, 0, thickness))
)
tab = tab.edges("|Z").chamfer(edge_chamfer)
tab = tab.faces(">Z").workplane().center(0, 0).rect(pocket_width, pocket_length).cutBlind(-pocket_depth)
tab = tab.faces(">Z").workplane().center(0, 0).rect(pocket_width, pocket_length).cutBlind(-pocket_depth)
result = base.union(tab)
result = result.edges("|Z").chamfer(edge_chamfer)
