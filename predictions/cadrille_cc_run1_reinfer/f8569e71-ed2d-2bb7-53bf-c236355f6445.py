import cadquery as cq
import math
outer_diameter = 40.0
inner_diameter = 20.0
thickness = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 0.5
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(thickness))
rib = (base.faces('>Z')
        .workplane()
        .center(0, 0)
        .rect(rib_width, rib_height)
        .extrude(thickness))
rib = rib.union(rib)
rib = rib.edges('|Z').chamfer(chamfer_size)
result = base.union(rib)
