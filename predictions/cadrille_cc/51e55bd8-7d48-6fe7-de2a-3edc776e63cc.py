import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 15.0
fillet_radius = 2.0
chamfer_distance = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 4
hole_offset = 10.0
rib_width = 10.0
rib_height = 5.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 4
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_width / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").fillet(fillet_radius)
combined = combined.edges("|Z").fillet(fillet_radius)
combined = (
    combined.faces(">Z")
    .workplane()
    .center(hole_offset, hole_offset)
    .hole(hole_diameter)
)
combined = combined.edges(">Z").fillet(fillet_radius)
result = combined
