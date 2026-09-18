import cadquery as cq
outer_radius = 45.0
inner_radius = 20.0
jaw_height = 30.0
boss_radius = 6.0
boss_height = 5.0
rib_width = 8.0
rib_height = 25.0
rib_thickness = 4.0
base = cq.Workplane('XY').circle(inner_radius).workplane(offset=jaw_height).circle(outer_radius).loft()
# boss on top face
boss = base.faces('>Z').workplane().circle(boss_radius).extrude(boss_height)
# rib on top face
rib = base.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
combined = base.union(boss).union(rib)
result = combined
