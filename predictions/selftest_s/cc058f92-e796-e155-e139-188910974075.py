import cadquery as cq
# Dimensions (max 100 units)
horizontal_leg_length = 80.0
vertical_leg_length = 70.0
bracket_thickness = 6.0
pocket_width = 20.0
pocket_depth = 4.0
pocket_offset_from_outer = 30.0
extrude_length = 12.0
chamfer_size = 0.5
mount_hole_dia = 5.0
mount_hole_spacing = 30.0
set_screw_dia = 3.0
counterbore_dia = 6.0
counterbore_depth = 5.0
counterbore_offset_from_bottom = 20.0
# Create L‑shape profile with rectangular pocket on horizontal leg
p1 = (0, 0)
p2 = (horizontal_leg_length, 0)
p3 = (horizontal_leg_length, bracket_thickness)
# pocket start x coordinate
pocket_start_x = horizontal_leg_length - pocket_offset_from_outer - pocket_width
p4 = (pocket_start_x + pocket_width, bracket_thickness)
# descend into pocket
p5 = (pocket_start_x + pocket_width, bracket_thickness - pocket_depth)
# left across pocket bottom
p6 = (pocket_start_x, bracket_thickness - pocket_depth)
# ascend back to thickness line
p7 = (pocket_start_x, bracket_thickness)
# continue to vertical leg
p8 = (bracket_thickness, bracket_thickness)
p9 = (bracket_thickness, vertical_leg_length)
p10 = (0, vertical_leg_length)
profile = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
result = cq.Workplane('XY').polyline(profile).close().extrude(extrude_length)
# Apply chamfer to all outer edges
result = result.edges().chamfer(chamfer_size)
# Mounting holes on horizontal leg (two holes)
horizontal_hole_y = bracket_thickness/2
horizontal_hole_x1 = horizontal_leg_length/3
horizontal_hole_x2 = 2*horizontal_leg_length/3
result = (result.faces('>Z')
          .workplane()
          .pushPoints([(horizontal_hole_x1, horizontal_hole_y), (horizontal_hole_x2, horizontal_hole_y)])
          .hole(mount_hole_dia))
# Mounting holes on vertical leg (two holes)
vertical_hole_x = bracket_thickness/2
vertical_hole_y1 = vertical_leg_length/3
vertical_hole_y2 = 2*vertical_leg_length/3
result = (result.faces('>Z')
          .workplane()
          .pushPoints([(vertical_hole_x, vertical_hole_y1), (vertical_hole_x, vertical_hole_y2)])
          .hole(mount_hole_dia))
# Counterbore for set screw on inner face of vertical leg (face with normal -X)
# Workplane on that face: Y axis = vertical direction, Z axis = extrude direction
counterbore_center_y = -vertical_leg_length/2 + counterbore_offset_from_bottom
result = (result.faces('<X')
          .workplane()
          .center(counterbore_center_y, 0)
          .cboreHole(set_screw_dia, counterbore_dia, counterbore_depth))