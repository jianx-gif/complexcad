import cadquery as cq
inner_wall_radius = 30.0
wall_thickness = 3.0
inner_wall_radius = wall_thickness
inner_wall_radius = inner_wall_radius - wall_thickness
inner_wall_height = 40.0
base = cq.Workplane('XY').circle(inner_wall_radius).extrude(base_thickness)
inner_cut = (
    cq.Workplane('XY')
    .polyline([
        (inner_wall_radius, 0),
        (inner_wall_radius, bellows_height),
        (inner_wall_radius, -inner_wall_height),
        (inner_wall_radius, -inner_wall_height + inner_wall_height),
        (inner_wall_radius, 0),
        (inner_wall_radius, 0)
    ])
    .close()
    .revolve(360)
)
base = base.cut(inner_cut)
rib = (
    cq.Workplane('XY')
    .box(rib_depth, inner_wall_radius, inner_wall_height)
    .translate((inner_wall_radius - inner_wall_radius, 0, 0))
)
base = base.union(rib)
base = base.edges().chamfer(0.5)
base = base.faces('>Z').edges().chamfer(0.5)
base = base.faces('>Z').edges().chamfer(0.5)
base = base.faces('>Z').edges().chamfer(0.5)
result = base
