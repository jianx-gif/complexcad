import cadquery as cq
outer_radius = 30.0
wall_thickness = 10.0
inner_radius = outer_radius - wall_thickness
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
base = base.cut(inner)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .translate((outer_radius - rib_spacing/2, 0, rib_count))
        .extrude(rib_height))
rib = rib.union(rib)
rib = (base.faces('>Z')
        .workplane()
        .center(0, 0)
        .rect(rib_width, rib_height)
        .extrude(rib_height))
result = base.union(rib)
