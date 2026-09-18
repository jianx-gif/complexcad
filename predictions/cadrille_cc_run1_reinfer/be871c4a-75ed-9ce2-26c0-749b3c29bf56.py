import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 1.0
base = cq.Workplane('XY').rect(leg_length, leg_width).extrude(thickness)
rib = (cq.Workplane('XY')
       .rect(leg_width, leg_length)
       .extrude(thickness))
rib = (base.faces('>Z')
       .workplane()
       .rect(rib_width, rib_height)
       .extrude(rib_height))
rib = (base.faces('>Z')
       .workplane()
       .rect(rib_width, rib_height)
       .extrude(rib_height))
rib = rib.union(rib)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, hole_offset),
    (hole_offset, hole_offset),
    (0, hole_offset),
    (0, -hole_offset),
]
result = leg
