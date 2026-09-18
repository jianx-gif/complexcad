import cadquery as cq
gear_thickness = 12.0
gear_thickness = gear_thickness - 2.0
gear_chamfer = 0.5
tip_chamfer = 0.5
pocket_width = 20.0
pocket_height = 4.0
pocket_depth = 10.0
shaft_radius = 5.0
set_screw_diameter = 3.0
set_screw_radius = shaft_radius + 2.0
set_screw_count = 6
set_screw_radius = shaft_radius + 2.0
gear_body = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(gear_thickness, 0)
    .lineTo(gear_thickness, gear_thickness)
    .lineTo(gear_thickness + gear_thickness, gear_thickness)
    .lineTo(gear_thickness + gear_thickness, gear_thickness)
    .lineTo(gear_thickness, gear_thickness)
    .close()
    .revolve()
)
gear_body = gear_body.faces(">Z").edges().chamfer(tip_chamfer)
tip_chamfered = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(set_screw_radius)
    .extrude(gear_thickness + 2.0)
)
gear_body = gear_body.cut(tip_chamfered)
gear_body = (
    gear_body
    .faces(">Z")
    .workplane()
    .polarArray(radius=set_screw_radius, count=set_screw_count, startAngle=0, angle=360)
    .hole(set_screw_diameter)
)
result = gear_body
