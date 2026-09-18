import cadquery as cq

plate_length = 100.0
plate_width = 80.0
plate_thickness = 8.0
rib_width = 10.0
rib_height = 6.0
hole_diameter = 6.0
hole_spacing_x = 20.0
hole_spacing_y = 30.0
hole_rows = 2
hole_cols = 4
edge_chamfer = 1.0
tab_length = 30.0
tab_width = 20.0
pocket_depth = 4.0
pocket_margin = 5.0

base_plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

tab = (
    cq.Workplane("XY")
    .center(0, plate_width / 2 + tab_width / 2)
    .rect(tab_length, tab_width)
    .extrude(plate_thickness)
)

plate_with_tab = base_plate.union(tab)

rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(plate_length, rib_width)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)

plate_with_rib = plate_with_tab.union(rib)

plate_chamfered = plate_with_rib.edges("|Z").chamfer(edge_chamfer)

hole_pattern = (
    plate_chamfered.faces(">Z")
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows)
    .hole(hole_diameter)
)

pocket = (
    hole_pattern.faces("<Z")
    .workplane()
    .rect(plate_length - 2 * pocket_margin, plate_width - 2 * pocket_margin)
    .cutBlind(-pocket_depth)
)

result = pocket