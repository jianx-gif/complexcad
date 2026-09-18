import cadquery as cq

# Parameters
base_radius = 30.0
base_height = 20.0
shoulder_step_height = 10.0
shoulder_radius = 45.0
total_height = base_height + shoulder_step_height + 5.0

groove_radius = 8.0
groove_center_offset = 35.0
chamfer_distance = 2.0

top_hole_diameter = 5.0
top_hole_head_diameter = 8.0
top_hole_head_height = 3.0
top_hole_count = 3
top_hole_radius = shoulder_radius - 5.0

# Base profile sketch in XZ plane
profile = (
    cq.Workplane('XZ')
    .lineTo(base_radius, 0)
    .lineTo(base_radius, base_height)
    .lineTo(shoulder_radius - shoulder_step_height, base_height)
    .lineTo(shoulder_radius - shoulder_step_height, base_height + shoulder_step_height)
    .lineTo(shoulder_radius, base_height + shoulder_step_height)
    .lineTo(shoulder_radius, total_height)
    .lineTo(0, total_height)
    .close()
)

# Revolve profile around Z axis
solid = profile.revolve()

# Cut arc groove using cylinder
groove_cyl = (
    cq.Workplane('XY')
    .cylinder(height=total_height + 10, radius=groove_radius)
    .translate((groove_center_offset, 0, -5))
)
solid = solid.cut(groove_cyl)

# Chamfer outer vertical edges
solid = solid.edges('|Z').chamfer(chamfer_distance)

# Top counterbore holes in polar array
result = (
    solid
    .faces('>Z')
    .workplane()
    .polarArray(radius=top_hole_radius, count=top_hole_count, startAngle=0, angle=360)
    .cboreHole(top_hole_diameter, top_hole_head_diameter, top_hole_head_height)
)
