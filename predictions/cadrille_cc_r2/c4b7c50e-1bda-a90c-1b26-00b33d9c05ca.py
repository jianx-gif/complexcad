import cadquery as cq
outer_radius = 45
inner_radius = 30
height = 80
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, height - height)
    .lineTo(inner_radius, height - height)
    .close()
    .revolve()
)
result = base
for i in range(1, len(inner_radius):
    angle = i * 360.0 / len(inner_radius
    rotated = (
        cq.Workplane("XY")
        .center(inner_radius + inner_radius, 0)
        .circle(inner_radius)
        .extrude(height)
        .translate((inner_radius + wall_thickness/2, 0, 0))
    )
    result = result.cut(rotated)
