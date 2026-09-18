import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 20.0
wall_thickness = 2.0
fillet_radius = 1.0
chamfer_distance = 0.5
rib_width = 4.0
rib_height = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 4
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .rect(outer_diameter, outer_diameter)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").fillet(fillet_radius)
combined = combined.edges("|Z").fillet(fillet_radius)
combined = (
    combined.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
combined = combined.edges(">Z").fillet(fillet_radius)
result = combined
