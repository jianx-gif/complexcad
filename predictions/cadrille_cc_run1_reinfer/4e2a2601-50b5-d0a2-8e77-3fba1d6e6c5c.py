import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
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
rib = rib.edges('|Z').chamfer(chamfer_size)
result = base.union(rib)
