import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 20.0
wall_thickness = 2.0
rib_width = 12.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)
rib = (
    cq.Workplane('XY')
    .rect(plate_length, rib_width)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
base = base.union(rib)
base = base.edges('|Z').chamfer(chamfer_size)
rib = (
    base.faces('>Z')
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.union(rib)
base = base.edges('|Z').chamfer(chamfer_size)
base = base.faces('>Z').edges().chamfer(chamfer_size)
base = base.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-rib_height)
base = base.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-rib_height)
base = base.faces('>Z').workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-rib_height)
result = base
