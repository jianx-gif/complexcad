import cadquery as cq
outer_diameter = 80.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = inner_diameter / 2.0
rib_width = 10.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_diameter / 2.0).extrude(wall_thickness)
rib = (cq.Workplane('XY')
        .circle(outer_diameter / 2.0)
        .extrude(wall_thickness))
rib = (base.faces('>Z')
        .workplane()
        .circle(inner_radius)
        .extrude(wall_thickness))
rib = (cq.Workplane('XY')
        .circle(inner_radius)
        .extrude(wall_thickness))
rib = (cq.Workplane('XY')
        .circle(inner_radius)
        .extrude(wall_thickness))
rib = rib.union(rib)
rib = rib.edges('|Z').chamfer(chamfer_size)
result = rib
