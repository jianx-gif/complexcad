import cadquery as cq
arm_length=80.0
arm_width=20.0
arm_thickness=8.0
wall_thickness=2.0
profile = (cq.Workplane('XY')
    .moveTo(0,0)
    .lineTo(arm_length-arm_width/2,0)
    .threePointArc((arm_length, arm_width/2),(arm_length-arm_width/2, arm_width))
    .lineTo(0, arm_width)
    .close())
outer = profile.extrude(arm_thickness)
outer = outer.shell(-wall_thickness)
result = outer