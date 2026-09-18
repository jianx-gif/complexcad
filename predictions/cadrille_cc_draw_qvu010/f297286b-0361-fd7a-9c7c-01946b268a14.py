import cadquery as cq
outer_diameter = 100.0
inner_diameter = 80.0
thickness = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 4
rib_radius = inner_diameter / 2.0
rib_height = 5.0
rib_spacing = 12.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0 - rib_spacing / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((outer_diameter / 2.0 - rib_spacing / 2.0, 0, 0))
rib = rib.translate((outer_diameter / 2.0 - rib_spacing / 2.0, 0, 0))
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
    .polarArray(radius=outer_diameter / 2.0 - rib_spacing / 2.0, startAngle=0, angle=360)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
combined = combined.union(rib)
result = (
    combined
    .faces(">Z")
    .workplane()
    .polarArray(radius=outer_diameter / 2.0 - rib_spacing / 2.0, startAngle=0, angle=360)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
