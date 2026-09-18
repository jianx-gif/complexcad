import cadquery as cq

overall_width = 80.0
overall_height = 60.0
overall_thickness = 6.0
shell_thickness = 1.5
gusset_height = 30.0
gusset_thickness = 8.0
gusset_offset = 20.0
clearance_slot_width = 7.0
clearance_slot_length = 40.0
clearance_slot_offset = 12.0
chamfer_distance = 0.8
slot_depth = overall_thickness / 2.0

base = cq.Workplane("XY").rect(overall_width, overall_height).extrude(overall_thickness)

gusset = (cq.Workplane("XY")
    .rect(gusset_thickness, gusset_height)
    .translate((overall_width/2 - gusset_thickness/2, gusset_offset - overall_height/2, 0))
    .extrude(overall_thickness)
)

combined = base.union(gusset)

shelled = combined.shell(-shell_thickness)

slot_center_x = 0.0
slot_center_y = (overall_height/2) - clearance_slot_offset - clearance_slot_length/2

shelled = (shelled.faces("<Z").workplane()
    .center(slot_center_x, slot_center_y)
    .rect(clearance_slot_width, clearance_slot_length)
    .cutBlind(-slot_depth)
)

result = shelled.edges("|Z").chamfer(chamfer_distance)
