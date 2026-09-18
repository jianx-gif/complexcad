import cadquery as cq
length = 80.0
width = 60.0
height = 40.0
shell_thickness = 2.0
stiffener_flange_width = 8.0
stiffener_depth = 12.0
stiffener_web_thickness = 3.0
stiffener_web_thickness = 3.0
stiffener_spacing = 15.0
stiffener_depth = stiffener_depth + 2.0
fillet_radius = 1.5
base = cq.Workplane('XY').box(length, width, height)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_web_thickness)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
stiffener = (
    cq.Workplane('XY')
    .center(stiffener_flange_width/2, 0)
    .rect(stiffener_depth, stiffener_web_thickness)
    .extrude(stiffener_depth)
)
)
result = (
    stiffener
    .edges('|Z')
    .fillet(fillet_radius)
)
