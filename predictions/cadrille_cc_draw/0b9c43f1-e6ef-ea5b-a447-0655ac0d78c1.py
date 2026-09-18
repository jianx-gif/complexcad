import cadquery as cq
outer_radius = 20.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
chamfer_distance = 0.5
hole_diameter = 4.0
hole_depth = 2.0
hole_count = 8
hole_spacing = 30.0
rib_width = 4.0
rib_height = 10.0
rib_thickness = 2.0
rib_count = 4
outer = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
inner = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(inner_radius)
)
inner = inner.cut(inner)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.translate((outer_radius - rib_thickness/2, 0, 0))
combined = outer.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_distance)
combined = combined.faces(">Z").edges().chamfer(chamfer_distance)
hole_positions = [
    (hole_spacing/2, hole_spacing/2),
    (hole_spacing/2, hole_spacing/2),
    (hole_spacing/2, hole_spacing/2),
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
