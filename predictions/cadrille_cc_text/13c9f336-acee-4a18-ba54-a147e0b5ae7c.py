import cadquery as cq
overall_width = 80.0
overall_height = 60.0
overall_thickness = 6.0
shell_thickness = 1.5
clearance_slot_width = 7.0
clearance_slot_length = 40.0
clearance_slot_height = 30.0
clearance_slot_offset = 20.0
chamfer_distance = 0.8
gusset_height = 30.0
gusset_thickness = 8.0
gusset_offset = 20.0
base = (
    cq.Workplane("XY")
    .rect(overall_width, overall_height)
    .extrude(overall_thickness)
)
shell = base.shell(-shell_thickness)
shell = shell.edges("|Z").chamfer(chamfer_distance)
shell = shell.faces(">Z").workplane().rect(overall_width - 2 * shell_thickness, overall_height - 2 * shell_thickness).cutBlind(-shell_thickness)
shell = shell.faces(">Z").workplane().rect(clearance_slot_width, clearance_slot_length).cutBlind(-clearance_slot_height)
shell = shell.faces(">Z").workplane().rect(clearance_slot_width, clearance_slot_length).cutBlind(-clearance_slot_height)
shell = shell.faces(">Z").workplane().rect(clearance_slot_width, clearance_slot_length).cutBlind(-clearance_slot_height)
shell = shell.faces(">Z").workplane().pushPoints([(0, -overall_height/2 + clearance_slot_offset), (0, -overall_height/2 + clearance_slot_offset)])
shell = shell.faces(">Z").workplane().pushPoints([(0, -overall_height/2 + clearance_slot_offset), (0, -overall_height/2 + clearance_slot_offset)])
shell = shell.faces(">Z").workplane().pushPoints([(0, -overall_height/2 + clearance_slot_offset), (0, -overall_height/2 + clearance_slot_offset)])
shell = shell.faces(">Z").workplane().pushPoints([(0, -overall_height/2 + clearance_slot_offset), (0, -overall_height/2 + clearance_slot_offset)])
shell = shell.faces("<Z").workplane().pushPoints([(0, -overall_height/2 + clearance_slot_offset), (0, -overall_height/2 + clearance_slot_offset)])
shell = shell.union(shell)
result = shell
