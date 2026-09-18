import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
wall_thickness = 2.0
inner_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
rib_width = 6.0
rib_height = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_diameter / 2.0).extrude(wall_thickness)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = (base.faces('>Z')
        .workplane()
        .center(inner_radius + rib_spacing, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = rib.union(rib)
rib = (cq.Workplane('XY')
        .center(inner_radius + rib_spacing, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = rib.union(rib)
rib = rib.edges('|Z').chamfer(chamfer_size)
result = rib
