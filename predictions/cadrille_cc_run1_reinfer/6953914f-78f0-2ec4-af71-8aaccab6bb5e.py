import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = (cq.Workplane('XY')
       .rect(rib_width, rib_height)
       .extrude(thickness))
rib = (base.faces('>Z')
       .workplane()
       .rect(rib_width, rib_height)
       .extrude(rib_thickness))
rib = rib.edges('|Z').chamfer(chamfer_size)
result = base.union(rib)
