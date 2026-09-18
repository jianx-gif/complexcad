import cadquery as cq
outer_radius = 40.0
inner_radius = 20.0
thickness = 5.0
rib_height = 2.0
rib_width = 4.0
rib_thickness = 2.0
rib_count = 6
rib_spacing = 12.0
chamfer_dist = 0.5
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_thickness/2, 0)
    .rect(rib_width, rib_thickness)
    .extrude(thickness)
)
rib = rib.translate((outer_radius - rib_thickness/2, 0, 0))
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_dist)
combined = combined.edges("|Z").chamfer(chamfer_dist)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = (
    combined.faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
combined = combined.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_dist)
result = combined
