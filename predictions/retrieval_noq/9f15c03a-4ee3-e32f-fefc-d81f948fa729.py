import cadquery as cq
import copy
from types import SimpleNamespace as Measures

outer_width = 80.0
outer_depth = 60.0
outer_height = 15.0
outer_chamfer = 2.0
corner_radius = 5.0

socket_width = 50.0
socket_depth = 40.0
socket_height = outer_height - 2.0

rib_thickness = 2.0
rib_spacing = 6.0
rib_height = socket_height - 1.0

mount_hole_dia = 5.0
mount_hole_offset = 18.0

outer = (
    cq.Workplane('XY')
    .center(-outer_width/2, -outer_depth/2)
    .polyline([
        (0, 0),
        (outer_width, 0),
        (outer_width, outer_depth - corner_radius),
        (outer_width - corner_radius, outer_depth),
        (corner_radius, outer_depth),
        (0, outer_depth - corner_radius),
        (0, 0)
    ])
    .close()
    .extrude(outer_height)
    .edges('>Z')
    .chamfer(outer_chamfer)
)

cavity = (
    cq.Workplane('XY')
    .center(-socket_width/2, -socket_depth/2)
    .rect(socket_width, socket_depth)
    .extrude(-socket_height)
    .edges('|Z')
    .fillet(1.0)
)

base = outer.cut(cavity)

rib_base = (
    cq.Workplane('XY')
    .center(-socket_width/2 + rib_spacing/2, -socket_depth/2 + rib_spacing/2)
    .rect(rib_thickness, socket_depth - rib_spacing)
    .extrude(rib_height)
    .translate((0, 0, outer_height - socket_height))
)

rib_count = int((socket_width - rib_spacing) // rib_spacing)
ribs = rib_base
for i in range(1, rib_count):
    ribs = ribs.union(rib_base.translate((i * rib_spacing, 0, 0)))

socket_with_ribs = base.union(ribs)

result = (
    socket_with_ribs.faces('>Y')
    .workplane(centerOption='CenterOfMass')
    .pushPoints([(-mount_hole_offset, 0), (mount_hole_offset, 0)])
    .hole(mount_hole_dia)
)
