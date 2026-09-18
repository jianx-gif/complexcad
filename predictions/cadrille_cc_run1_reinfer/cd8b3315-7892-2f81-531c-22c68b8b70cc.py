import cadquery as cq
import math
outer_radius = 40.0
inner_radius = 30.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_count = 4
hole_offset = 10.0
base = cq.Workplane('XY').circle(outer_radius).extrude(wall_thickness)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = (base.faces('>Z')
        .workplane()
        .hole(hole_diameter)
        .edges()
        .chamfer(chamfer_distance)
    )
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .extrude(wall_thickness))
rib = rib.edges('|Z').fillet(inner_radius)
rib = rib.edges('>Z').chamfer(chamfer_distance)
result = rib
