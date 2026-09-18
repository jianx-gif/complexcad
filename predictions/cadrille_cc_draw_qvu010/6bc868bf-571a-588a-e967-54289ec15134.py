import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 5.0
rib_height = 12.0
rib_width = 8.0
rib_depth = 4.0
rib_count = 6
rib_count = 6
rib_radius = inner_diameter / 2.0
rib_height = wall_thickness + rib_height
rib_count = 4
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
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
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(rib_height)
)
rib = rib.translate((inner_radius + rib_depth / 2.0, 0, rib_height / 2.0))
)
rib = rib.translate((inner_radius + rib_depth / 2.0, 0, rib_height / 2.0))
rib = rib.translate((inner_radius + rib_depth / 2.0, 0, rib_height / 2.0))
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([
        (inner_radius + rib_radius, 0),
        (inner_radius + rib_radius, rib_height),
        (inner_radius + rib_radius, rib_height),
        (inner_radius, rib_height),
    ])
    .rect(rib_width, rib_height)
    )
    .extrude(rib_height)
)
combined = combined.union(rib)
result = combined
