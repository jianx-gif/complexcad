import cadquery as cq
body_length = 80
body_diameter = 40
wall_thickness = 4
inlet_diameter = 20
outlet_thread_major = 20
outlet_thread_minor = 16
thread_len = 10
conical_length = 40
fillet_radius = 2
chamfer_size = 1
top_flange_height = 5
hole_diameter = 5
hole_pitch_angle = 120
inlet_radius = inlet_diameter/2 + wall_thickness
straight_len = body_length - conical_length - thread_len - top_flange_height
outer = (cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(0, straight_len)
    .lineTo(inlet_radius, straight_len)
    .threePointArc((inlet_radius + fillet_radius, straight_len + fillet_radius),
                   (outlet_thread_major/2, straight_len + conical_length))
    .lineTo(outlet_thread_major/2, straight_len + conical_length + thread_len)
    .lineTo(outlet_thread_major/2, straight_len + conical_length + thread_len + top_flange_height)
    .lineTo(0, straight_len + conical_length + thread_len + top_flange_height)
    .close()
    .revolve()
)
inlet_cyl = cq.Workplane('XY').circle(inlet_diameter/2).extrude(straight_len)
cone = cq.Solid.makeCone(inlet_diameter/2, outlet_thread_minor/2, conical_length).translate((0, 0, straight_len))
outlet_cyl = cq.Workplane('XY').circle(outlet_thread_minor/2).extrude(thread_len).translate((0, 0, straight_len + conical_length))
inner = inlet_cyl.union(cone).union(outlet_cyl)
body = outer.cut(inner)
body = body.faces('>Z').edges().chamfer(chamfer_size)
hole = cq.Workplane('XY').circle(hole_diameter/2).extrude(body_length)
hole_cyl = hole.translate((body_diameter/2 - wall_thickness/2, 0, 0))
holes = cq.Workplane('XY')
for angle in [0, hole_pitch_angle, 2*hole_pitch_angle]:
    holes = holes.union(hole_cyl.rotate((0,0,0), (0,0,1), angle))
body = body.cut(holes)
result = body