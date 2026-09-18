import cadquery as cq

# Parameters
plate_width = 90.0
plate_depth = 60.0
plate_thickness = 6.0
pocket_width = 40.0
pocket_depth = 30.0
pocket_offset_x = 20.0
pocket_offset_y = 15.0
slot_width = 8.0
slot_length = 30.0
slot_offset_from_edge = 5.0
hole_diameter = 4.0
hole_radius = hole_diameter / 2.0
hole_grid_rows = 2
hole_grid_cols = 4
hole_grid_spacing_x = 20.0
hole_grid_spacing_y = 25.0
hole_grid_origin_x = (plate_width - (hole_grid_cols - 1) * hole_grid_spacing_x) / 2.0
hole_grid_origin_y = (plate_depth - (hole_grid_rows - 1) * hole_grid_spacing_y) / 2.0
edge_chamfer = 0.8

result = (
    cq.Workplane("XY")
    .box(plate_width, plate_depth, plate_thickness)
    .edges("|Z").chamfer(edge_chamfer)
    .faces(">Z").workplane()
    # Rectangular pocket cut through the plate thickness
    .center(pocket_offset_x - plate_width / 2 + pocket_width / 2,
            pocket_offset_y - plate_depth / 2 + pocket_depth / 2)
    .rect(pocket_width, pocket_depth)
    .cutBlind(-plate_thickness)
    # Side slot cut from one edge
    .workplane(offset=-plate_thickness / 2)
    .center(-plate_width / 2 + slot_offset_from_edge + slot_width / 2,
            0)
    .slot2D(slot_length, slot_width, 0)
    .cutBlind(-plate_thickness)
    # Drilling pattern of eight M4 holes on top surface
    .workplane(offset=plate_thickness / 2)
    .center(-plate_width / 2 + hole_grid_origin_x,
            -plate_depth / 2 + hole_grid_origin_y)
    .rarray(hole_grid_spacing_x, hole_grid_spacing_y, hole_grid_cols, hole_grid_rows)
    .hole(hole_radius)
)
