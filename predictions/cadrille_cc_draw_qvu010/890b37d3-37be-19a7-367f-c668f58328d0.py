import cadquery as cq
plate_width = 100.0
plate_height = 80.0
plate_thickness = 4.0
rib_height = 2.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset_from_end = 15.0
chamfer_size = 0.5
base = cq.Workplane('XY').box(plate_width, plate_height, plate_thickness)
rib = (
    cq.Workplane('XY')
    .box(plate_width, plate_height, plate_thickness)
    .translate((0, 0, plate_thickness))
)
rib = rib.faces('>Z').workplane().hole(hole_diameter)
rib = rib.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).extrude(rib_height)
rib = rib.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).extrude(rib_height)
rib = rib.union(rib)
hole_positions = [
    (-plate_width/2 + hole_offset_from_end, -plate_height/2 + hole_offset_from_end),
    ( plate_width/2 - hole_offset_from_end, -plate_height/2 + hole_offset_from_end),
    (-plate_width/2 + hole_offset_from_end,  plate_height/2 - hole_offset_from_end),
    ( plate_width/2 - hole_offset_from_end,  plate_height/2 - hole_offset_from_end),
]
result = rib
