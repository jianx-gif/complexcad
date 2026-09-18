import cadquery as cq

outer_diameter = 80
wall_thickness = 5
inner_diameter = outer_diameter - 2 * wall_thickness
body_length = 100
split_groove_width = 20
split_groove_depth = 4
inlet_diameter = 10
outlet_diameter = 12
chamfer_size = 1
flange_extra_dia = 30
flange_thickness = 8
channel_width = 6
channel_height = 30
channel_offset = 10

outer = cq.Workplane('XY').circle(outer_diameter / 2).extrude(body_length)
inner = cq.Workplane('XY').circle(inner_diameter / 2).extrude(body_length)
body = outer.cut(inner)

flange = cq.Workplane('XY').circle((outer_diameter + flange_extra_dia) / 2).extrude(flange_thickness)
body = body.union(flange.translate((0, 0, body_length)))

groove = (
    cq.Workplane('XY')
    .box(split_groove_depth, body_length, split_groove_width)
    .translate((outer_diameter / 2 - split_groove_depth / 2, 0, 0))
)
body = body.cut(groove)

body = body.faces('>Z').workplane().hole(inlet_diameter)
body = body.faces('<Z').workplane().hole(outlet_diameter)
body = body.edges('|Z').chamfer(chamfer_size)

channel = (
    cq.Workplane('XY')
    .box(channel_width, body_length - 2 * channel_offset, inner_diameter / 2 - wall_thickness - channel_width / 2)
    .translate((0, 0, channel_offset + channel_width / 2))
)
body = body.cut(channel)

result = body.split(cq.Plane.YZ)
