import cadquery as cq

leg_length = 70
leg_width = 20
leg_thickness = 8
gusset_height = 20
pilot_hole_diameter = 4
pilot_hole_offset = 5
chamfer_size = 1

l_shape = (
    cq.Workplane('XY')
    .lineTo(leg_length, 0)
    .lineTo(leg_length, leg_width)
    .lineTo(leg_width, leg_width)
    .lineTo(leg_width, leg_length)
    .lineTo(0, leg_length)
    .close()
    .extrude(leg_thickness)
)

gusset = (
    cq.Workplane('XY')
    .center(leg_width, leg_width)
    .polyline([(0, 0), (gusset_height, 0), (0, gusset_height)])
    .close()
    .extrude(leg_thickness)
)

result = (
    l_shape.union(gusset)
    .faces('>Z')
    .workplane()
    .center(leg_width + pilot_hole_offset, leg_width + pilot_hole_offset)
    .hole(pilot_hole_diameter)
    .edges()
    .chamfer(chamfer_size)
)
