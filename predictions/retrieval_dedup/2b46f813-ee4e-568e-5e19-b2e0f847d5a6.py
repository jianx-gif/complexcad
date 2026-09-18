import cadquery as cq

outer_diameter = 60
inner_diameter = 30
body_length = 40
flange_diameter = 80
flange_thickness = 12
bolt_hole_diameter = 8
bolt_hole_pitch = 30
num_bolt_holes = 4
groove_diameter = 40
groove_thickness = 4
keyway_width = 8
keyway_depth = 8
chamfer_size = 2

body = cq.Workplane('XY').circle(outer_diameter/2).extrude(body_length)
flange = cq.Workplane('XY').circle(flange_diameter/2).extrude(flange_thickness).translate((0,0,body_length))
result = body.union(flange)
result = result.hole(inner_diameter)
keyway = (cq.Workplane('XY')
          .center(outer_diameter/2 - keyway_depth/2, 0)
          .rect(keyway_depth, keyway_width)
          .extrude(body_length + flange_thickness))
result = result.cut(keyway)
result = result.workplane(offset=body_length/2).circle(groove_diameter/2).cutBlind(-groove_thickness)
result = (result.faces('>Z')
          .workplane()
          .polarArray(bolt_hole_pitch, 0, 360, num_bolt_holes)
          .hole(bolt_hole_diameter))
result = result.edges('|Z').chamfer(chamfer_size)
