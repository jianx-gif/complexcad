import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 15.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 4
base = cq.Workplane('XY').box(leg_length, leg_width, thickness)
base = base.edges('|Z').chamfer(chamfer_size)
hole_positions = [
    (hole_offset, leg_width/2 - hole_offset),
    (-hole_offset, leg_width/2 - hole_offset),
    (hole_offset, leg_width/2 - hole_offset),
    (-hole_offset, leg_width/2 - hole_offset),
    (hole_offset, leg_width/2 - hole_offset),
]
base = base.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
rib = (
    cq.Workplane('XY')
    .box(rib_width, rib_height, thickness)
    .translate((leg_width/2 - rib_thickness/2, leg_width/2, thickness/2))
)
base = base.union(rib)
base = base.faces('>Z').workplane().center(leg_width/2, leg_width/2).rect(leg_width, leg_width).cutBlind(-thickness)
base = base.faces('>Z').workplane().center(leg_width/2, leg_width/2).rect(rib_width, rib_height).cutBlind(-thickness)
base = base.faces('>Z').workplane().center(leg_width/2, leg_width/2).rect(rib_width, rib_height).cutBlind(-thickness)
base = base.edges('|Z').chamfer(chamfer_size)
result = base
