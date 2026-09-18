import cadquery as cq
panel_length = 90
panel_width = 60
panel_thickness = 4
slot_width = 2
slot_length = 70
slot_spacing = 8
stiff_rib_width = 5
stiff_rib_depth = 2
stiff_rib_spacing = 12
chamfer_size = 0.5
mount_hole_dia = 4
mount_hole_offset = 10
stiff_rib_width = 5
stiff_rib_depth = 2
stiff_rib_spacing = 12
result = cq.Workplane("XY").rect(panel_length, panel_width).extrude(panel_thickness)
result = result.faces(">Z").workplane().center(0, 0).rect(stiff_rib_width, panel_width).cutBlind(-panel_thickness)
result = result.faces(">Z").workplane().center(0, 0).rect(stiff_rib_width, panel_width).cutBlind(-panel_thickness)
result = result.faces(">Z").workplane().center(0, 0).rect(stiff_rib_width, panel_width).cutBlind(-panel_thickness)
result = result.faces(">Z").workplane().center(0, 0).hole(stiff_rib_width, depth=stiff_rib_depth)
result = result.faces(">Z").workplane().center(0, 0).rect(stiff_rib_width, panel_width).cutBlind(-stiff_rib_depth)
