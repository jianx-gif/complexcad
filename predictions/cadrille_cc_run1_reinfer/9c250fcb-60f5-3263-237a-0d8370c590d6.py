import cadquery as cq
plate_length = 80.0
plate_width = 40.0
plate_thickness = 8.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 4.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 0.5
base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)
rib = (cq.Workplane('XY')
       .rect(rib_width, plate_width - 2 * rib_spacing)
       .extrude(rib_height))
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
