import cadquery as cq
import math
outer_diameter = 30.0
inner_diameter = 20.0
height = 12.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
chamfer_distance = 0.5
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(height)
inner_cyl = cq.Workplane('XY').circle(inner_diameter/2).extrude(height)
base = base.cut(inner_cyl)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(rib_thickness)
        .translate((0, 0, height/2 - rib_thickness/2))
    )
base = base.union(rib)
rib = (base.faces('>Z')
        .workplane()
        .center(0, 0)
        .rect(rib_width, rib_height)
        .extrude(rib_thickness))
rib = rib.union(rib)
rib = (base.faces('>Z')
        .workplane()
        .center(0, 0)
        .rect(rib_width, rib_height)
        .extrude(rib_thickness))
result = base.union(rib)
