import cadquery as cq
plate_width = 80.0
plate_height = 60.0
plate_thickness = 5.0
tab_width = 20.0
tab_length = 10.0
hole_diameter = 6.0
blind_hole_depth = 3.0
hole_count = 6
hole_spacing = (plate_width - 2 * hole_diameter) / (hole_count - 1)
edge_chamfer = 0.5
tab_width = 20.0
tab_length = 40.0
tab_thickness = 5.0
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .edges("|Z")
    .chamfer(edge_chamfer)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(tab_width, tab_length)
    .cutBlind(-plate_thickness)
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(tab_width, tab_length)
    .cutBlind(-plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_spacing/2, hole_spacing/2),
        (hole_spacing/2, -hole_spacing/2),
        (hole_spacing/2, -hole_spacing/2),
        (hole_spacing/2, hole_spacing/2),
        (hole_spacing/2, hole_spacing/2),
        (hole_spacing/2, hole_spacing/2)
    ])
    .hole(hole_diameter)
)
