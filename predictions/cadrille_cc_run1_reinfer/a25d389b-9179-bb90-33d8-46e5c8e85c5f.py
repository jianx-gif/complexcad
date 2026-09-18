import cadquery as cq
outer_radius = 45
inner_radius = 30
wall_thickness = 5
inner_radius = inner_radius - wall_thickness
rib_width = 20
rib_height = 10
rib_thickness = 4
rib_spacing = 12
chamfer_size = 1
base = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
base = base.cut(inner)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .translate((outer_radius - rib_thickness/2, 0, 0))
        .extrude(rib_height))
rib = rib.union(rib)
rib = rib.edges('|Z').chamfer(chamfer_size)
result = base.union(rib)
