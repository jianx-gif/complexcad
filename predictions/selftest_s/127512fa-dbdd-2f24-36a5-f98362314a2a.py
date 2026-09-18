import cadquery as cq

width = 80.0
height = 60.0
thickness = 8.0
flange_width = 20.0
slot_length = 30.0
slot_width = 10.0
mount_hole_dia = 5.0
mount_hole_cbore_dia = 8.0
mount_hole_cbore_depth = 2.0
central_hole_dia = 12.0
fillet_radius = 1.5

base = cq.Workplane('XY').rect(width, height).extrude(thickness)
slot_cut = cq.Workplane('XY').center(0, 0).rect(slot_length, slot_width).extrude(thickness + 2)
base = base.cut(slot_cut)
hole_positions = [(-width/2 + flange_width/2, height/4), (width/2 - flange_width/2, height/4), (0, -height/2 + thickness/2)]
base = base.faces('>Z').workplane().pushPoints(hole_positions).cboreHole(mount_hole_dia, mount_hole_cbore_dia, mount_hole_cbore_depth)
base = base.faces('>Z').workplane().center(0, 0).hole(central_hole_dia)
result = base.edges('((>X or <X) and |Z)').fillet(fillet_radius)
