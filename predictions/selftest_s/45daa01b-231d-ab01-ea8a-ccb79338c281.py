import cadquery as cq
import math

outer_diameter = 70.0
inner_diameter = 30.0
collar_length = 30.0
flange_extension = 10.0
flange_thickness = 5.0
set_screw_diameter = 5.0
countersink_angle = 90.0
chamfer_distance = 1.0
relief_width = 12.0
relief_depth = 4.0
knurl_pocket_width = 2.0
knurl_pocket_depth = 1.0
knurl_rows = 3
knurl_cols = 5
knurl_spacing = 6.0

base = cq.Workplane('XY').circle(outer_diameter/2).extrude(collar_length)
flange = cq.Workplane('XY').circle((outer_diameter/2)+flange_extension).extrude(flange_thickness)
flange = flange.translate((0,0,collar_length-flange_thickness))
body = base.union(flange)
inner_bore = cq.Workplane('XY').circle(inner_diameter/2).extrude(collar_length+0.01)
body = body.cut(inner_bore)

cs_radius = set_screw_diameter/2
countersink_depth = cs_radius / math.tan(math.radians(countersink_angle/2))
set_screw_length = flange_thickness + 2.0
set_screw = (cq.Workplane('YZ')
    .circle(cs_radius)
    .extrude(set_screw_length))
set_screw = set_screw.translate(((outer_diameter/2)+(flange_extension/2), 0, collar_length - flange_thickness/2))
body = body.cut(set_screw)

countersink_solid = cq.Solid.makeCone(cs_radius, cs_radius*2, countersink_depth)
countersink = (cq.Workplane('XY')
    .add(countersink_solid)
    .rotate((0,0,0), (0,1,0), 90)
    .translate(((outer_diameter/2)+(flange_extension/2), 0, collar_length - flange_thickness/2)))
body = body.cut(countersink)

slot = (cq.Workplane('YZ')
    .rect(relief_width, relief_depth)
    .extrude(outer_diameter/2 + flange_extension + 1))
slot = slot.translate((0, 0, collar_length/2))
body = body.cut(slot)

body = body.edges('|Z').fillet(chamfer_distance)

pocket = (cq.Workplane('YZ')
    .rect(knurl_pocket_width, knurl_pocket_depth)
    .extrude(knurl_pocket_width+0.5))
pocket = pocket.rotate((0,0,0), (0,0,1), 90)
patterns = []
for i in range(knurl_rows):
    for j in range(knurl_cols):
        x_offset = (outer_diameter/2) + 0.2
        y_offset = (i - (knurl_rows-1)/2) * knurl_spacing
        z_offset = (j - (knurl_cols-1)/2) * knurl_spacing + collar_length/2
        p = pocket.translate((x_offset, y_offset, z_offset))
        patterns.append(p)
knurl_pattern = patterns[0]
for p in patterns[1:]:
    knurl_pattern = knurl_pattern.union(p)
body = body.cut(knurl_pattern)

result = body