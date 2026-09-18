
import cadquery as cq

cover_dia = 80
wall_thk = 4
boss_rad = 15
boss_h = 8
hole_dia = 6
tab_w = 6
tab_h = 12
tab_cnt = 4
fillet_r = 4
overlap = 1

# Base plate
base = cq.Workplane('XY').circle(cover_dia/2).extrude(wall_thk)

# Raised boss on top of base
boss = (cq.Workplane('XY')
        .circle(boss_rad)
        .extrude(boss_h)
        .translate((0, 0, wall_thk)))

body = base.union(boss)

# Central through hole
hole = (cq.Workplane('XY')
        .circle(hole_dia/2)
        .extrude(wall_thk + boss_h + 2)
        .translate((0, 0, -1)))
body = body.cut(hole)

# Tab profile: rectangular tab extending radially outward and intersecting base
x_offset = cover_dia/2 - overlap + tab_w/2

tab = (cq.Workplane('XY')
       .rect(tab_w, tab_h)
       .extrude(wall_thk + 1)
       .translate((x_offset, 0, -0.5)))

# Add tabs around perimeter
for i in range(tab_cnt):
    angle = i * 360/tab_cnt
    tab_i = tab.rotate((0,0,0), (0,0,1), angle)
    body = body.union(tab_i)

# Fillet outer rim edges on top face and boss top edge
body = body.faces('>Z').edges().fillet(fillet_r)

result = body
