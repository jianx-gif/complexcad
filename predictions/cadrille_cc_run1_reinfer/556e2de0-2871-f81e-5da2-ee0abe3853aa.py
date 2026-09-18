import cadquery as cq
outer_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
rib_width = 10.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = (base.faces('>Z')
        .workplane()
        .center(0, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = rib.union(rib)
rib = (base.faces('>Z')
        .workplane()
        .center(0, 0)
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
result = rib
