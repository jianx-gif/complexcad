import cadquery as cq
cover_length = 80
cover_width = 60
cover_height = 12
wall_thickness = 2
rim_chamfer = 1
rib_height = 4
rib_width = 30
rib_depth = cover_width - 2 * wall_thickness
lip_width = 2
lip_thickness = 1
vent_hole_dia = 3
vent_spacing_x = 10
vent_spacing_y = 12
vent_columns = 4
vent_rows = 3
base = cq.Workplane('XY').box(cover_length, cover_width, cover_height)
shell = base.shell(-wall_thickness).edges().chamfer(rim_chamfer)
rib = (cq.Workplane('XY')
    .box(rib_width, rib_depth, rib_height)
    .translate((0, 0, -cover_height/2 + wall_thickness + rib_height/2)))
lip = (cq.Workplane('XY')
    .box(cover_length + 2*lip_width, cover_width + 2*lip_width, lip_thickness)
    .translate((0, 0, cover_height/2 - lip_thickness/2)))
body = shell.union(rib).union(lip)
result = (body.faces('>Z')
    .workplane()
    .rarray(vent_spacing_x, vent_spacing_y, vent_columns, vent_rows, center=True)
    .circle(vent_hole_dia/2)
    .cutBlind(-cover_height))