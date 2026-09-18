import cadquery as cq
leg_width = 20.0
wall_thickness = 2.0
inner_radius = 10.0
hole_diameter = 5.0
hole_spacing_long = 15.0
hole_spacing_short = 15.0
hole_rows = 2
hole_cols = 3
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, leg_width)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius + wall_thickness, leg_width + wall_thickness)
    .lineTo(inner_radius + wall_thickness, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width + wall_thickness)
    .lineTo(inner_radius, leg_width)
    .lineTo(inner_radius, 0)
    .close()
    .extrude(leg_width)
)
result = base
