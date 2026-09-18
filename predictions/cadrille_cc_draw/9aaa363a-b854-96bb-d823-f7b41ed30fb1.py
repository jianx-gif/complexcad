import cadquery as cq
plate_length = 80.0
plate_width = 60.0
plate_thickness = 10.0
rib_height = 8.0
rib_width = 12.0
rib_spacing = 15.0
rib_count = 6
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, plate_width)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib = rib.translate((0, 0, plate_thickness))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(hole_diameter)
combined = (
    combined.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, rib_width)
    .extrude(rib_height)
)
combined = combined.union(rib)
hole_positions = [
    (-plate_length/2 + hole_offset, -plate_width/2 + hole_offset),
    ( plate_length/2 - hole_offset, -plate_width/2 + hole_offset),
    (-plate_length/2 + hole_offset,  plate_width/2 - hole_offset),
    ( plate_length/2 - hole_offset,  plate_width/2 - hole_offset)
]
combined = (
    combined.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined
