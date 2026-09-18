import cadquery as cq
import math
plate_length = 80.0
plate_width = 80.0
plate_thickness = 5.0
rib_width = 5.0
rib_height = 3.0
central_hole_dia = 30.0
clearance_hole_dia = 7.0
clearance_hole_count = 6
clearance_hole_radius = 25.0
edge_chamfer = 0.5
rib_chamfer = 0.3
slot_width = 8.0
slot_length = 20.0
pocket_reduction = 20.0
base = (cq.Workplane("XY")
        .rect(plate_length, plate_width)
        .extrude(plate_thickness))
outer_rib = (cq.Workplane("XY")
            .rect(plate_length, plate_width)
            .extrude(rib_height)
            .translate((0, 0, plate_thickness)))
inner_rib_cut = (cq.Workplane("XY")
                .rect(plate_length - 2 * rib_width, plate_width - 2 * rib_width)
                .extrude(rib_height)
                .translate((0, 0, plate_thickness)))
rib = outer_rib.cut(inner_rib_cut)
result = base.union(rib)
result = result.faces(">Z").workplane().hole(central_hole_dia)
points = [(clearance_hole_radius * math.cos(math.radians(i * 360 / clearance_hole_count)),
           clearance_hole_radius * math.sin(math.radians(i * 360 / clearance_hole_count)))
          for i in range(clearance_hole_count)]
result = result.faces(">Z").workplane().pushPoints(points).hole(clearance_hole_dia)
depth = plate_thickness + rib_height
result = result.faces(">Y").workplane().rect(slot_length, slot_width).cutBlind(-depth)
result = result.faces("<Y").workplane().rect(slot_length, slot_width).cutBlind(-depth)
result = result.faces("<Z").workplane().rect(plate_length - pocket_reduction, plate_width - pocket_reduction).cutBlind(-2)
result = result.edges("|Z").chamfer(edge_chamfer)
