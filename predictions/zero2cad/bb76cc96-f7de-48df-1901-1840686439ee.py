import cadquery as cq
lever_length = 80.0
lever_width = 20.0
lever_thickness = 8.0
tip_radius = 10.0
base = (
    cq.Workplane('XY')
    .moveTo(0, -lever_width/2)
    .lineTo(lever_length - tip_radius, -lever_width/2)
    .threePointArc((lever_length, 0), (lever_length - tip_radius, lever_width/2))
    .lineTo(0, lever_width/2)
    .close()
    .extrude(lever_thickness)
)
result = base
