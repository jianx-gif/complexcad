import cadquery as cq

plate_length = 80.0
plate_width = 70.0
plate_thickness = 8.0
slot_width = 12.0
slot_length = 45.0
slot_spacing = 25.0
hole_diameter = 6.0
hole_spacing = 20.0
rib_width = 6.0
rib_height = 15.0
rib_offset = 10.0
chamfer_size = 0.8

base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)

slot_centers = [(-slot_spacing, 0), (0, 0), (slot_spacing, 0)]
base = base.faces('>Z').workplane().pushPoints(slot_centers).rect(slot_width, slot_length).cutBlind(-plate_thickness)

hole_centers = [(-hole_spacing, 0), (0, 0), (hole_spacing, 0)]
base = base.faces('>Z').workplane().pushPoints(hole_centers).hole(hole_diameter)

rib = cq.Workplane('XY').rect(rib_width, rib_height).extrude(plate_thickness)
rib = rib.translate((rib_offset, 0, -plate_thickness))
base = base.union(rib)

result = base.edges('|Z').chamfer(chamfer_size)
