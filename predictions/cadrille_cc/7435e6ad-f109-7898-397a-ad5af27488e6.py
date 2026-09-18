import cadquery as cq
import math
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 13.0
rib_width = 5.0
rib_height = 8.0
rib_spacing = 12.0
rib_count = 4
chamfer_size = 1.0
mount_hole_diameter = 5.0
mount_hole_offset = 10.0
base = cq.Workplane('XY').rect(outer_diameter, outer_diameter).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((0, outer_diameter/2 + rib_width/2, 0))
rib = rib.translate((0, outer_diameter/2 + rib_width/2, 0))
rib = rib.translate((0, outer_diameter/2 + rib_width/2, 0))
rib = rib.translate((0, outer_diameter/2 + rib_width/2, 0))
rib = rib.translate((0, outer_diameter/2 + rib_width/2, 0))
rib = rib.translate((0, outer_diameter/2 + rib_width/2, 0))
result = base.union(rib)
result = result.faces('>Z').workplane().hole(mount_hole_diameter)
result = result.edges('|Z').chamfer(chamfer_size)
