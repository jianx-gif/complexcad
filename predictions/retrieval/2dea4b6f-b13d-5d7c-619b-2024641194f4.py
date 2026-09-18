import cadquery as cq
import math

outer_radius = 30.0
inner_radius = 15.0
collar_thickness = 10.0
split_groove_width = 2.0
split_groove_depth = 2.0
split_groove_position = 4.0
knurl_count = 12
knurl_radius = 1.0
knurl_depth = 1.0
set_screw_dia = 2.5
set_screw_offset = 5.0
bevel_height = 2.0

result = (cq.Workplane('XY')
          .circle(outer_radius)
          .extrude(collar_thickness))

inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(collar_thickness)
result = result.cut(inner_cyl)

groove = (cq.Workplane('XY')
          .circle(outer_radius - split_groove_depth)
          .extrude(split_groove_width)
          .translate((0, 0, split_groove_position)))
result = result.cut(groove)

result = (result
          .faces('>Z')
          .workplane()
          .center(outer_radius - set_screw_offset, 0)
          .hole(set_screw_dia))

knurl_template = (cq.Workplane('XY')
                 .circle(knurl_radius)
                 .extrude(collar_thickness)
                 .val())
knurl_solids = []
for i in range(knurl_count):
    angle = math.radians(i * 360.0 / knurl_count)
    x = (outer_radius - knurl_depth/2) * math.cos(angle)
    y = (outer_radius - knurl_depth/2) * math.sin(angle)
    knurl_solids.append(knurl_template.translate((x, y, 0)))
knurl_compound = cq.Compound.makeCompound(knurl_solids)
result = result.cut(knurl_compound)

bevel = cq.Solid.makeCone(inner_radius, inner_radius - bevel_height, bevel_height)
bevel = bevel.translate((0, 0, collar_thickness - bevel_height))
result = result.cut(bevel)
