import cadquery as cq
outer_diameter = 80.0
thickness = 5.0
fillet_radius = 2.0
hole_diameter_base = 4.0
hole_count = 6
hole_spacing = 12.0
mount_hole_dia = 5.0
mount_offset = 10.0
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - fillet_radius
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
filleted = base.edges("|Z").fillet(fillet_radius)
hole_positions = [
    (hole_count-1.5, hole_count+1.5),
    (-hole_count+1.5, hole_count+1.5),
    (hole_count+1.5, hole_count+1.5),
    (-hole_count+1.5, hole_count+1.5),
]
for x, y in hole_positions:
    filleted = (
        cq.Workplane("XY")
        .center(x, y)
        .circle(hole_diameter_base)
        .extrude(thickness)
    )
    filleted = filleted.edges("|Z").chamfer(fillet_radius)
result = filleted
