import cadquery as cq
import math
outer_radius = 40.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = inner_radius - wall_thickness
chamfer_distance = 0.5
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 4
base = cq.Workplane('XY').circle(outer_radius).extrude(outer_radius)
inner = cq.Workplane('XY').circle(inner_radius).extrude(outer_radius)
base = base.cut(inner)
rib = (cq.Workplane('XY')
        .rect(rib_width, rib_height)
        .translate((outer_radius - rib_spacing/2, 0, 0))
        .extrude(rib_height))
rib = rib.union(rib)
rib = rib.edges().chamfer(chamfer_distance)
rib = (base.faces('>Z')
        .workplane()
        .center(0, 0)
        .rect(rib_width, rib_height)
        .extrude(rib_height))
result = base.union(rib)
