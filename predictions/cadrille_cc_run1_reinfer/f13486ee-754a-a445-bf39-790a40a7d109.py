import cadquery as cq
outer_radius = 40.0
inner_radius = 20.0
wall_thickness = 2.0
rib_width = 10.0
rib_height = 8.0
rib_thickness = 3.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 30.0
hole_offset = 10.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = (base.faces('>Z')
        .workplane()
        .hole(inner_radius * 2)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = rib.union(rib)
rib = rib.edges('|Z').chamfer(chamfer_size)
result = base.union(rib)
