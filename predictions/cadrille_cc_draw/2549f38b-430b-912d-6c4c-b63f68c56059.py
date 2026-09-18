import cadquery as cq
plate_length = 100.0
plate_width = 30.0
plate_thickness = 8.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset_from_edge = 10.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(plate_length - 2 * rib_spacing, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = (
    rib.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, plate_width - 2 * rib_spacing)
    .extrude(rib_height)
)
combined = base.union(rib)
hole_positions = [
    (-plate_length/2 + hole_offset_from_edge, -plate_width/2 + hole_offset_from_edge),
    ( plate_length/2 - hole_offset_from_edge, -plate_width/2 + hole_offset_from_edge),
    (-plate_length/2 + hole_offset_from_edge,  plate_width/2 - hole_offset_from_edge),
    ( plate_length/2 - hole_offset_from_edge,  plate_width/2 - hole_offset_from_edge)
]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = combined.edges(">Z").chamfer(chamfer_size)
