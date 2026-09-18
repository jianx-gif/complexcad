import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
chamfer_distance = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = hole_diameter / 2.0
hole_offset = outer_radius - wall_thickness/2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)
result = (
    profile
    .faces(">Z")
    .workplane()
    .hole(hole_diameter)
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, count=6, startAngle=0, angle=360)
    .hole(hole_diameter)
)
