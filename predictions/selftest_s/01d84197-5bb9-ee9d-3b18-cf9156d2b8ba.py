import cadquery as cq
import math

outer_radius = 40
hub_radius = 15
thickness = 30
groove_depth = 8
groove_width = 12
groove_center_z = thickness / 2
shaft_bore_radius = 8
fillet_radius = 1
screw_shaft_radius = 2
countersink_base_radius = 3
countersink_depth = 5
mount_hole_radius = 1.5
mount_circle_radius = hub_radius * 0.6

base = (cq.Workplane('XZ')
        .moveTo(outer_radius, 0)
        .lineTo(outer_radius, thickness)
        .lineTo(hub_radius, thickness)
        .lineTo(hub_radius, 0)
        .close()
        .revolve())

groove = (cq.Workplane('XZ')
          .moveTo(outer_radius - groove_depth, groove_center_z - groove_width / 2)
          .lineTo(outer_radius - groove_depth, groove_center_z + groove_width / 2)
          .lineTo(outer_radius, groove_center_z + groove_width / 2)
          .lineTo(outer_radius, groove_center_z - groove_width / 2)
          .close()
          .revolve())
base = base.cut(groove)

shaft_bore = (cq.Workplane('XY')
              .circle(shaft_bore_radius)
              .extrude(thickness))
base = base.cut(shaft_bore)
base = base.edges('>Z').fillet(fillet_radius)

ccone = cq.Solid.makeCone(countersink_base_radius, screw_shaft_radius, countersink_depth)
ccone = ccone.rotate((0, 0, 0), (0, 1, 0), 90).translate((outer_radius, 0, thickness / 2))
base = base.cut(ccone)

mount_points = []
for i in range(4):
    angle = i * 90
    x = mount_circle_radius * math.cos(math.radians(angle))
    y = mount_circle_radius * math.sin(math.radians(angle))
    mount_points.append((x, y))
base = (base
        .faces('>Z')
        .workplane()
        .pushPoints(mount_points)
        .hole(mount_hole_radius * 2))

base = base.edges().fillet(0.5)

result = base