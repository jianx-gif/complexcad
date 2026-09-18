import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 2.0
inner_radius = inner_radius - wall_thickness
rib_width = 10.0
rib_height = 8.0
rib_thickness = 4.0
rib_spacing = 12.0
chamfer_size = 1.0
base = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
base = base.cut(inner)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .translate((outer_radius - rib_thickness/2, 0, 0))
        .extrude(rib_height))
rib = rib.union(rib)
rib = rib.edges().chamfer(chamfer_size)
result = base.union(rib)
