import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 8.0
rib_width = 12.0
rib_height = 6.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 1.0
base = cq.Workplane('XY').rect(leg_length, leg_width).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .rect(leg_width, leg_width)
    .extrude(thickness)
    .translate((leg_length/2 - rib_width/2, leg_width/2, 0))
)
combined = base.union(rib)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, hole_offset),
]
result = (
    combined
    .faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
