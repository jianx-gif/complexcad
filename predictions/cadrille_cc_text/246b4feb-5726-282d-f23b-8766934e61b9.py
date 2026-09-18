import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
corner_hole_diameter = 6.0
corner_counter_diameter = 10.0
corner_counter_diameter = 12.0
edge_chamfer = 0.8
central_hole_diameter = 8.0
central_hole_depth = plate_thickness - 2.0
pocket_depth = 3.0
pocket_spacing = 15.0
pocket_rows = 2
pocket_cols = 3
pocket_spacing = 15.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
    .edges("|Z")
    .chamfer(edge_chamfer)
)
rib_fillet = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(central_hole_diameter / 2)
    .extrude(rib_height)
)
base = base.union(rib_fillet)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cskHole(central_hole_diameter, central_hole_diameter, central_counter_diameter, plate_thickness, plate_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cskHole(central_hole_diameter, central_hole_diameter, central_counter_diameter, plate_thickness, plate_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .cskHole(central_hole_diameter, central_hole_diameter, central_counter_diameter, plate_thickness, plate_thickness, plate_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_spacing, pocket_cols)
    .extrude(pocket_depth)
)
result = base
