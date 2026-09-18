import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 10.0
rib_width = 6.0
rib_height = 8.0
rib_thickness = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 6
chamfer_size = 1.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(thickness))
rib = (base.faces('>Z')
        .workplane()
        .center(0, 0)
        .rect(rib_width, rib_height)
        .extrude(thickness))
rib = rib.union(rib)
rib = rib.edges('|Z').chamfer(chamfer_size)
result = base.union(rib)
