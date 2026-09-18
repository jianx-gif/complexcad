import cadquery as cq
import math
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 15.0
rib_width = 10.0
rib_height = 5.0
rib_thickness = 2.0
hole_diameter = 5.0
hole_spacing = 20.0
chamfer_size = 1.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(thickness)
rib = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.edges().chamfer(chamfer_size)
rib = rib.faces('>Z').workplane().hole(hole_diameter)
rib = rib.faces('>Z').workplane().hole(hole_diameter)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces('>Z').workplane().rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.translate((0, 0, thickness))
result = rib.union(rib)
