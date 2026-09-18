import cadquery as cq
plate_length = 80.0
plate_width = 50.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
chamfer_distance = 1.0
bolt_hole_diameter = 5.0
bolt_hole_spacing = 30.0
pocket_width = 20.0
pocket_height = 10.0
pocket_depth = 4.0
pocket_depth = plate_thickness - 2.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_spacing, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
combined = base.union(rib)
combined = (
    combined.faces(">Z").workplane()
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)
combined = (
    combined.faces(">Z").workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)
combined = combined.edges("|Z").chamfer(chamfer_distance)
result = combined
