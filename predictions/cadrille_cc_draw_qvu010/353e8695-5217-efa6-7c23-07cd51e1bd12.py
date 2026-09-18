import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 5.0
rib_height = 12.0
rib_width = 8.0
rib_length = 20.0
rib_count = 6
rib_count = 4
rib_radius = inner_diameter / 2.0
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_diameter)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(rib_height)
)
rib = rib.translate((inner_radius, 0, rib_height / 2.0))
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .polarArray(radius=inner_radius - wall_thickness / 2.0, count=rib_count, startAngle=0, angle=360)
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
combined = combined.union(rib)
result = (
    combined
    .faces(">Z")
    .workplane()
    .polarArray(radius=inner_radius - wall_thickness / 2.0, startAngle=0, angle=360)
    .hole(inner_diameter)
)
