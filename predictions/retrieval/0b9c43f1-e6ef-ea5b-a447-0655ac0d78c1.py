import cadquery as cq, math
casing_outer_radius = 30.0
wall_thickness = 4.0
casing_length = 60.0
inlet_flange_length = 12.0
flange_thickness = 6.0
outlet_lip_extension = 8.0
outlet_lip_height = 4.0
chamfer_size = 1.0
bolt_hole_diameter = 4.0
bolt_circle_radius = 22.0
num_bolt_holes = 4

outer = (cq.Workplane('XY')
    .moveTo(casing_outer_radius, 0)
    .lineTo(casing_outer_radius, inlet_flange_length)
    .lineTo(casing_outer_radius + flange_thickness, inlet_flange_length)
    .lineTo(casing_outer_radius + flange_thickness, inlet_flange_length + casing_length)
    .threePointArc((casing_outer_radius + flange_thickness + outlet_lip_extension, inlet_flange_length + casing_length + outlet_lip_height),
                  (casing_outer_radius, inlet_flange_length + casing_length))
    .close())

outer_solid = outer.revolve()

inner_radius = casing_outer_radius - wall_thickness
inner_cylinder = (cq.Workplane('XY')
    .circle(inner_radius)
    .extrude(inlet_flange_length + casing_length + outlet_lip_extension + outlet_lip_height + 2*flange_thickness))

shell = outer_solid.cut(inner_cylinder)

shell = shell.faces('>Z').edges().chamfer(chamfer_size)

bolt_face = shell.faces('>Z')
# create points around circle for bolt holes
angles = [i*2*math.pi/num_bolt_holes for i in range(num_bolt_holes)]
points = [(bolt_circle_radius*math.cos(a), bolt_circle_radius*math.sin(a)) for a in angles]
result = (bolt_face.workplane(offset=flange_thickness/2)
    .pushPoints(points)
    .hole(bolt_hole_diameter))
