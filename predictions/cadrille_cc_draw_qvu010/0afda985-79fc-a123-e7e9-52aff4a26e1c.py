import cadquery as cq
import math
plate_width = 30.0
plate_height = 10.0
plate_thickness = 5.0
rib_height = 2.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 6
hole_diameter = 4.0
hole_spacing = 15.0
chamfer_distance = 0.5
rib_count = int((plate_width - rib_spacing) // rib_count)
base = cq.Workplane('XY').rect(plate_width, plate_height).extrude(plate_thickness)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, plate_height)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
rib = rib.union(rib)
result = base.union(rib)
result = result.faces('>Z').edges().chamfer(chamfer_distance)
result = result.faces('>Z').workplane().hole(hole_diameter)
result = result.faces('>Z').workplane().center(0, 0).hole(hole_diameter)
result = result.faces('>Z').workplane().center(0, 0).hole(hole_diameter)
result = result.faces('>Z').workplane().center(0, 0).hole(hole_diameter)
