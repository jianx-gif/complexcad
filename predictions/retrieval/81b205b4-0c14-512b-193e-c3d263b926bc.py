import cadquery as cq
from types import SimpleNamespace as Measures
p = Measures(plate_width=70, plate_depth=60, plate_thickness=6, chamfer=0.8, boss_radius=10, boss_height=8, fillet_radius=0.5)
base = cq.Workplane('XY').box(p.plate_width, p.plate_depth, p.plate_thickness).translate((0,0,p.plate_thickness/2)).edges().chamfer(p.chamfer)
boss = base.faces('>Z').workplane().circle(p.boss_radius).extrude(p.boss_height).edges('>Z').fillet(p.fillet_radius)
result = base.union(boss)
