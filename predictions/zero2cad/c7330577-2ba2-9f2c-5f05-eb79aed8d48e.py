import cadquery as cq

outer_diameter = 60.0
wall_thickness = 4.0
height = 40.0
latch_width = 12.0
latch_height = 8.0
latch_thickness = 3.0
latch_offset = 20.0
boss_diameter = 10.0
boss_height = 6.0
chamfer_size = 0.5

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(height)
base_shell = outer_cyl.cut(inner_cyl)

latch = (
    cq.Workplane('XY')
    .box(latch_thickness, latch_width, latch_height)
    .translate((outer_radius + latch_thickness/2.0 - 0.2, 0, latch_offset + latch_height/2.0))
)

boss = (
    cq.Workplane('XY')
    .center(inner_radius - boss_diameter/2.0 + 0.2, 0)
    .circle(boss_diameter/2.0)
    .extrude(boss_height)
)

result = base_shell.union(latch).union(boss)
result = result.faces('>Z').edges().chamfer(chamfer_size)
