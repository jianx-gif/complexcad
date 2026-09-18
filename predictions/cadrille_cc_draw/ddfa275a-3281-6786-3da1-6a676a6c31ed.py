import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
wall_thickness = 5.0
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_count = 6
hole_radius = inner_diameter / 2.0
hole_count = 4
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2.0, 0)
    .lineTo(inner_diameter / 2.0, wall_thickness)
    .lineTo(inner_diameter / 2.0 + wall_thickness, wall_thickness)
    .lineTo(inner_diameter / 2.0 + wall_thickness, wall_thickness + wall_thickness)
    .lineTo(inner_diameter / 2.0, wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_diameter / 2.0, wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_diameter / 2.0, wall_thickness + wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_diameter / 2.0, wall_thickness + wall_thickness + wall_thickness + wall_thickness)
    .lineTo(inner_diameter / 2.0, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + 0.5
    .lineTo(inner_diameter / 2.0, wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + wall_thickness + radi
    .lineTo(inner_diameter / 2.0, wall_thickness + wall_thickness + wall_thickness + wall_thickness + radi
    .lineTo(inner_diameter / 2.0, wall_thickness + wall_thickness + wall_thickness + radi
    .lineTo(inner_diameter / 2.0, wall_thickness + wall_thickness + wall_thickness + radi
    .lineTo(inner_diameter / 2.0, wall_thickness + wall_thickness + wall_thickness + radi
    .close()
)
result = (
    cq.Workplane("XY")
    .polarArray(radius=inner_diameter / 2.0, startAngle=0, angle=360)
    .hole(hole_diameter)
)
