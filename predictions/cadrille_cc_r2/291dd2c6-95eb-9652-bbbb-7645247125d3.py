import cadquery as cq
outer_radius = 45
inner_radius = 20
height = 15
wall_thickness = 2
chamfer_distance = 0.5
hole_diameter = 5
hole_spacing = 30
hole_count = 6
hole_count = 4
hole_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, height - height)
    .lineTo(inner_radius, height - height)
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
    .polarArray(radius=hole_radius, count=hole_count, startAngle=0, angle=360)
    .hole(hole_diameter)
)
