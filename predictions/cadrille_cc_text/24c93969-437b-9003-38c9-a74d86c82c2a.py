import cadquery as cq
outer_diameter = 80.0
plate_thickness = 8.0
slot_width = 5.0
slot_length = 20.0
outer_radius = outer_diameter / 2.0
slot_center_z = plate_thickness / 2.0
slot_center_z = plate_thickness / 2.0
slot_center_y = slot_center_z + slot_length / 2.0
base = cq.Workplane('XY').circle(outer_radius).extrude(plate_thickness)
slot = cq.Workplane('XY').rect(slot_width, slot_length).extrude(plate_thickness)
slot = slot.edges().chamfer(slot_center_y)
slot = slot.edges().chamfer(slot_center_y)
result = base.cut(slot)
