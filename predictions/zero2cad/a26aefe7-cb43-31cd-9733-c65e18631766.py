import cadquery as cq
base_width=60.0
base_height=30.0
tab_width=15.0
tab_height=10.0
thickness=8.0
result = (
    cq.Workplane('XY')
    .moveTo(-base_width/2, -base_height/2)
    .lineTo(base_width/2, -base_height/2)
    .lineTo(base_width/2, base_height/2)
    .lineTo(base_width/2 + tab_width, base_height/2)
    .lineTo(base_width/2 + tab_width, base_height/2 + tab_height)
    .lineTo(base_width/2, base_height/2 + tab_height)
    .lineTo(-base_width/2, base_height/2)
    .close()
    .extrude(thickness)
)
