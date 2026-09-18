import cadquery as cq
plate_length = 80.0
plate_width = 80.0
plate_thickness = 8.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
hole_diameter = 4.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 1.0
base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)
rib = (cq.Workplane('XY')
       .rect(plate_length - 2 * rib_spacing, plate_width - 2 * rib_spacing)
       .extrude(rib_height))
rib = (cq.Workplane('XY')
       .rect(plate_length - 2 * rib_spacing, plate_width - 2 * rib_spacing)
       .extrude(rib_height))
rib = rib.union(rib)
rib = rib.edges('|Z').chamfer(chamfer_size)
result = base.union(rib)
