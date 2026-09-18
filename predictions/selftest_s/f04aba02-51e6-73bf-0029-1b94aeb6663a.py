import cadquery as cq

panel_width = 80.0
panel_height = 60.0
panel_thickness = 4.0
corner_fillet_radius = 2.0
rib_width = 20.0
rib_length = 40.0
rib_thickness = 3.0
slot_width = 30.0
slot_height = 5.0
hole_diameter = 5.0
hole_rows = 4
hole_cols = 5
hole_spacing_x = 12.0
hole_spacing_y = 12.0
edge_hole_diameter = 3.0
edge_hole_count = 6
edge_hole_spacing = 12.0
edge_offset = 5.0

# Base panel
result = (cq.Workplane("XY")
    .rect(panel_width, panel_height)
    .extrude(panel_thickness))

# Corner fillets on vertical edges
result = result.edges("|Z").fillet(corner_fillet_radius)

# Cable slot cutout on top surface
result = (result.faces("+Z")
    .workplane()
    .center(0, -panel_height/2 + slot_height/2 + edge_offset)
    .rect(slot_width, slot_height)
    .cutBlind(-panel_thickness))

# Rectangular array of through holes (representing threaded holes)
hole_origin_x = - (hole_cols - 1) * hole_spacing_x / 2
hole_origin_y = - (hole_rows - 1) * hole_spacing_y / 2
result = (result.faces("+Z")
    .workplane()
    .center(hole_origin_x, hole_origin_y)
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows)
    .hole(hole_diameter))

# Linear array of edge holes along top edge of panel
result = (result.faces("+Z")
    .workplane()
    .center(0, panel_height/2 - edge_offset)
    .rarray(edge_hole_spacing, 0, edge_hole_count, 1)
    .hole(edge_hole_diameter))

# Central reinforcement rib on top face (added after hole operations)
rib = (cq.Workplane("XY")
    .rect(rib_width, rib_length)
    .extrude(rib_thickness))
result = result.union(rib.translate((0, 0, panel_thickness)))
