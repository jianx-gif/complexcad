import cadquery as cq
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
height = 15.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_count = 6
hole_radius = outer_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, height - fillet_radius)
    .threePointArc((outer_radius + fillet_radius, height - fillet_radius), (outer_radius, height))
    .lineTo(outer_radius, height - fillet_radius)
    .threePointArc((outer_radius, height), (outer_radius, 0))
    .close()
    .revolve()
)
result = (
    profile
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, count=hole_count, startAngle=0, angle=360)
    .hole(hole_diameter)
)
