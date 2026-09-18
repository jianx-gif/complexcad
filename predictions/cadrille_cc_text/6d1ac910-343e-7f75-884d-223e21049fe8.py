import cadquery as cq
panel_width = 100.0
panel_height = 70.0
panel_thickness = 4.0
corner_radius = 6.0
chamfer_dist = 1.0
hole_diameter = 4.0
countersink_diameter = 8.0
countersink_angle = 60.0
hole_row_spacing = 15.0
hole_col_spacing = 10.0
extrude = 1.0
hole_offset_x = -panel_width/2 + corner_radius + 2.0
hole_offset_y = -panel_thickness/2
hole_rows = 2
hole_cols = 3
hole_spacing = (panel_width - 2 * hole_row_spacing) / (hole_cols - 1)
hole_points = [
    (hole_offset_x, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing),
    (panel_width/2, -panel_height/2 + hole_row_spacing)
]
result = cq.Workplane("XY").polyline(hole_points).close().extrude(panel_thickness)
result = result.edges().chamfer(chamfer_dist)
result = result.faces(">Z").workplane().center(hole_offset_x, 0).rect(hole_cols*hole_spacing).cutBlind(-panel_thickness)
