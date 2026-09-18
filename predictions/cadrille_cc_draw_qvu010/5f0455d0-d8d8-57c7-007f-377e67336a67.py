import cadquery as cq
arm_length = 100.0
arm_width = 30.0
arm_thickness = 5.0
arm_height = 12.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
base = cq.Workplane('XY').box(arm_length, arm_width, arm_thickness)
arm = base.faces('>Z').workplane().center(0, 0).rect(arm_length, arm_width).extrude(arm_thickness)
arm = arm.edges('|Z').chamfer(chamfer_size)
arm = arm.faces('>Z').workplane().center(0, 0).rect(arm_length, arm_width).extrude(arm_thickness)
arm = arm.faces('>Z').workplane().center(0, 0).rect(arm_length, arm_width).cutBlind(-arm_thickness)
result = arm
