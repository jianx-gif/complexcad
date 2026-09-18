import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 8.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 4.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 1.0
base = cq.Workplane('XY').box(leg_length, leg_width, thickness)
rib = (cq.Workplane('XY')
       .rect(rib_width, leg_width)
       .extrude(thickness)
       .translate((leg_length/2, leg_width/2, thickness/2))
       .rotate((0,0,0), (0,0,1), rib_thickness)
       .translate((leg_length/2, leg_width/2, thickness/2))
       .rotate((0,0,0), (0,0,1), rib_thickness))
ribs = rib
for i in range(rib_count):
    angle = i * 360.0 / rib_count
    rib_i = rib.rotate((0,0,0), (0,0,1), angle)
    ribs = ribs.union(rib_i)
hole_positions = [
    (-hole_offset, -hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, hole_offset),
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
]
result = (
    base
    .faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
