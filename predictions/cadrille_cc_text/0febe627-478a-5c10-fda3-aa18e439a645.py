import cadquery as cq
cover_length = 80.0
cover_width = 60.0
cover_height = 12.0
wall_thickness = 2.0
rim_chamfer = 1.0
vent_hole_dia = 3.0
vent_spacing_x = 10.0
vent_spacing_y = 12.0
rib_height = 4.0
rib_width = 30.0
rib_length = cover_length - 2 * wall_thickness
lip_width = 2.0
lip_thickness = 1.0
lip_thickness = wall_thickness
result = cq.Workplane('XY').box(cover_length, cover_width, cover_height, centered=(True, True, False))
result = result.shell(-wall_thickness)
result = result.faces('>Z').workplane().center(0, 0).circle(vent_hole_dia / 2).cutBlind(-wall_thickness)
result = result.faces('>Z').workplane().center(0, 0).circle(vent_hole_dia / 2).cutBlind(-wall_thickness)
result = result.faces('>Z').workplane().center(0, 0).circle(vent_hole_dia / 2).cutBlind(-wall_thickness)
result = result.faces('>Z').workplane().center(0, 0).circle(vent_hole_dia / 2).cutBlind(-wall_thickness)
result = result.faces('>Z').edges().chamfer(rim_chamfer)
