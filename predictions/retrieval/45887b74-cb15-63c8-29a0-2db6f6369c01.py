import cadquery as cq

leg_length_horizontal = 80.0
leg_length_vertical = 60.0
bracket_thickness = 8.0
bracket_depth = 8.0
pocket_width = 6.0
pocket_height = 20.0
pocket_cut_depth = 4.0
pocket_offset_x = bracket_thickness / 2
pocket_offset_y = leg_length_vertical / 2
hole_diameter = 4.0
hole_spacing = 20.0
number_of_holes = 4
chamfer_distance = 0.5

L_profile = [
    (0, 0),
    (leg_length_horizontal, 0),
    (leg_length_horizontal, bracket_thickness),
    (bracket_thickness, bracket_thickness),
    (bracket_thickness, leg_length_vertical),
    (0, leg_length_vertical),
]

result = cq.Workplane("XY").polyline(L_profile).close().extrude(bracket_depth)
result = result.edges().chamfer(chamfer_distance)
result = result.faces(">Z").workplane().center(pocket_offset_x, pocket_offset_y).rect(pocket_width, pocket_height).cutBlind(-pocket_cut_depth)
result = result.faces(">Z").workplane().center(leg_length_horizontal/2, bracket_thickness/2).rarray(hole_spacing, 0, number_of_holes, 1).hole(hole_diameter)
