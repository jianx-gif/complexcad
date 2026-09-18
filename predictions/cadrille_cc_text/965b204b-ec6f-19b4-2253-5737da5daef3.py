import cadquery as cq
plate_length = 70.0
plate_width = 30.0
thickness = 3.0
chamfer = 2.0
rib_width = 10.0
rib_height = 20.0
rib_offset = 20.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_spacing = 12.0
fillet_radius = 1.0
base = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_height, thickness)
    .translate((0, 0, thickness))
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
combined = combined.edges("|Z").chamfer(chamfer)
result = combined
