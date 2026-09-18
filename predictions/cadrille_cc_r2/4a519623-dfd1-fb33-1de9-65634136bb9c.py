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
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)
result = (
    base
    .faces(">Z")
    .workplane()
    .hole(inner_radius * 2)
    .faces(">Z")
    .workplane()
    .polarArray(radius=outer_radius - wall_thickness/2, startAngle=0, angle=360, count=4)
    .hole(inner_radius * 2)
    .faces("<Z")
    .workplane()
    .polarArray(radius=outer_radius - wall_thickness/2, startAngle=0, angle=360, count=4)
    .hole(inner_radius * 2)
)
