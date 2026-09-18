import cadquery as cq
rail_length = 100.0
rail_width = 30.0
base_thickness = 8.0
rib_height = 3.0
rib_width = 12.0
hole_diameter = 2.0
hole_spacing = 18.0
edge_chamfer = 0.8
boss_dia = 8.0
boss_height = 6.0
base = cq.Workplane('XY').box(rail_width, rail_length, base_thickness)
rib = (
    cq.Workplane('XY')
    .box(rail_width - 2 * rib_width, rail_length - 2 * rib_width, base_thickness)
    .translate((0, 0, base_thickness/2))
)
base = base.union(rib)
boss = (
    cq.Workplane('XY')
    .box(boss_dia, boss_height, base_thickness)
    .translate((0, 0, base_thickness/2 + boss_height/2))
)
base = base.union(boss)
hole_positions = [
    (rail_length/2 - hole_spacing/2, rail_length/2 - hole_spacing/2),
    (-rail_length/2 + hole_spacing/2, rail_length/2 - hole_spacing/2),
    (rail_length/2 - hole_spacing/2, -rail_length/2 + hole_spacing/2),
    (-rail_length/2 + hole_spacing/2, -rail_length/2 + hole_spacing/2),
    (rail_length/2 - hole_spacing/2, -rail_length/2 + hole_spacing/2)
]
base = base.union(boss)
boss = (
    cq.Workplane('XY')
    .box(boss_dia, boss_height, base_thickness)
    .translate((rail_length/2 - boss_height/2, 0, base_thickness/2))
)
base = base.union(boss)
base = base.edges('|Z').chamfer(edge_chamfer)
result = base
