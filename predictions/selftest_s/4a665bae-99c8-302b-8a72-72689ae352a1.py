import cadquery as cq

guide_length = 80
guide_width = 30
guide_height = 20
wall_thickness = 4
tab_width = 12
tab_thickness = 5
tab_height = 8
chamfer_size = 1
hole_diameter = 4
port_radius = 6
port_gap = 0.8

outer = cq.Workplane("XY").rect(guide_width, guide_height).extrude(guide_length)
inner = cq.Workplane("XY").rect(guide_width - 2*wall_thickness, guide_height - 2*wall_thickness).extrude(guide_length + 2).translate((0,0,-1))
body = outer.cut(inner)

tab = cq.Workplane("XY").rect(tab_thickness, tab_width).extrude(tab_height)
tab = tab.translate((guide_width/2 + tab_thickness/2, 0, (guide_length - tab_height)/2))
body = body.union(tab)

cyl1 = cq.Workplane("YZ").center(-port_gap/2,0).circle(port_radius).extrude(guide_width + 2).translate((0,0,guide_length/2))
cyl2 = cq.Workplane("YZ").center(port_gap/2,0).circle(port_radius).extrude(guide_width + 2).translate((0,0,guide_length/2))
body = body.cut(cyl1).cut(cyl2)

body = body.faces(">Z").edges().chamfer(chamfer_size)

hole_positions = [(guide_length/4, 0), (3*guide_length/4, 0)]
body = body.faces(">X").workplane().pushPoints(hole_positions).hole(hole_diameter)

result = body