import cadquery as cq
cover_dia = 80.0
wall_thk = 4.0
boss_rad = 15.0
boss_h = 8.0
fillet_r = 4.0
hole_dia = 6.0
hole_count = 4
hole_spacing = cover_dia/2 - wall_thk/2
tab_h = 12.0
tab_w = 6.0
boss_rad = boss_rad + boss_rad/2
boss_h = boss_rad + boss_rad/2
profile = (
    cq.Workplane("XY")
    .circle(cover_dia/2)
    .extrude(cover_dia/2)
)
solid = profile.extrude(cover_dia/2)
solid = solid.faces(">Z").workplane().circle(boss_rad).extrude(boss_h)
solid = solid.edges("|Z").fillet(fillet_r)
tab = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(tab_w, tab_h)
    .extrude(tab_w)
)
solid = solid.union(tab)
solid = solid.edges(">Z").fillet(fillet_r)
hole_positions = [
    (hole_count-1.0, hole_count-1.0),
    (hole_count-1.0, hole_count-1.0),
    (hole_count-1.0, hole_count-1.0),
]
solid = (
    solid.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .circle(boss_rad + boss_h/2)
    .extrude(boss_h/2)
)
solid = solid.cut(hole_positions)
result = solid
