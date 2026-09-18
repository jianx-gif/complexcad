import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 30.0
rib_width = 5.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_depth = 10.0
hole_count = 6
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((outer_radius - rib_thickness / 2.0, 0, 0))
combined = base.union(rib)
hole_positions = [
    (inner_radius + rib_spacing, 0),
    (-inner_radius + rib_spacing, 0),
    (inner_radius, 0),
    (-inner_radius, -inner_radius),
    (inner_radius, -inner_radius),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
