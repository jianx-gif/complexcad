import cadquery as cq
cover_length = 80
cover_width = 60
cover_thickness = 5
hinge_width = 10
hinge_flex_thickness = 1
mounting_groove_depth = 1
mounting_groove_width = 3
rib_thickness = 0.8
rib_spacing = 5
pocket_depth = 2
chamfer_size = 0.1
hole_diameter = 3
hole_offset = 10

base = cq.Workplane('XY').rect(cover_length, cover_width).extrude(cover_thickness)

groove = (cq.Workplane('XY')
    .rect(cover_length - 2*mounting_groove_width, cover_width - 2*mounting_groove_width)
    .extrude(-mounting_groove_depth))
result = base.cut(groove)

hinge_cut = (cq.Workplane('XY')
    .transformed(offset=(cover_length/2 - hinge_width/2, 0, hinge_flex_thickness))
    .rect(hinge_width, cover_width)
    .extrude(cover_thickness - hinge_flex_thickness))
result = result.cut(hinge_cut)

num_ribs = int(cover_width/(rib_spacing + rib_thickness))
for i in range(num_ribs):
    y_pos = -cover_width/2 + (rib_spacing + rib_thickness)/2 + i*(rib_spacing + rib_thickness)
    rib = (cq.Workplane('XY')
        .transformed(offset=(cover_length/2 - hinge_width/2 - rib_thickness, y_pos, 0))
        .rect(rib_thickness, rib_spacing)
        .extrude(cover_thickness))
    result = result.union(rib)

pocket_block = (cq.Workplane('XY')
    .center(0,0)
    .rect(cover_length - 2*mounting_groove_width - 20, cover_width - 2*mounting_groove_width - 20)
    .extrude(pocket_depth)
    .translate((0,0, cover_thickness - pocket_depth)))
result = result.cut(pocket_block)

result = result.edges('|Z').chamfer(chamfer_size)

hole_positions = [
    (-cover_length/2 + hole_offset, -cover_width/2 + hole_offset),
    (cover_length/2 - hole_offset, -cover_width/2 + hole_offset),
    (-cover_length/2 + hole_offset, cover_width/2 - hole_offset),
    (cover_length/2 - hole_offset, cover_width/2 - hole_offset)
]
holes = (cq.Workplane('XY')
    .pushPoints(hole_positions)
    .circle(hole_diameter/2)
    .extrude(cover_thickness + 0.1))
result = result.cut(holes)
