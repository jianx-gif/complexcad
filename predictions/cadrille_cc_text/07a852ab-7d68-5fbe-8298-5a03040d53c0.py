import cadquery as cq
cover_radius = 40.0
wall_thickness = 5.0
cover_height = 20.0
lip_height = 3.0
lip_thickness = 2.0
vent_radius = 8.0
vent_depth = 4.0
clearance_hole_radius = 2.0
chamfer_distance = 1.0
outer_radius = cover_radius + wall_thickness
outer_radius = cover_radius - wall_thickness
inner_radius = cover_radius - wall_thickness
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(cover_height)
lip = cq.Workplane('XY').circle(outer_radius).extrude(lip_thickness)
lip = lip.faces('>Z').edges().chamfer(chamfer_distance)
lip = lip.faces('>Z').edges().chamfer(chamfer_distance)
lip = lip.faces('>Z').edges().chamfer(chamfer_distance)
lip = lip.faces('>Z').edges().chamfer(chamfer_distance)
lip = lip.faces('>Z').edges().chamfer(chamfer_distance)
lip = lip.faces('>Z').edges().chamfer(chamfer_distance)
lip = lip.faces('>Z').edges().chamfer(chamfer_distance)
lip = lip.faces('>Z').edges().chamfer(chamfer_distance)
lip = lip.faces('>Z').edges().chamfer(chamfer_distance)
lip = lip.faces('>Z').edges().chamfer(chamfer_distance)
lip = lip.faces('>Z').edges().chamfer(chamfer_distance)
lip = lip
for i in range(1, 2):
    angle = 360.0 / vent_depth
    y = cover_radius * math.cos(angle)
    y = cover_radius * math.sin(angle)
    hole = (
        cq.Workplane('XZ')
        .box(outer_radius * 2, outer_radius * 2, outer_radius * 2, centered=False)
        .translate((0, y, y))
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    hole = hole.cut(hole)
result = l
