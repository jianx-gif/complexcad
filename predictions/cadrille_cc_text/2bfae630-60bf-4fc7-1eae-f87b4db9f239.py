import cadquery as cq
body_length = 60.0
outer_radius = 20.0
inlet_radius = 10.0
wall_thickness = 3.0
rib_width = 4.0
rib_height = 6.0
fillet_radius = 2.0
inlet_radius = inlet_radius - wall_thickness
rib_count = int((body_length - rib_width) // rib_height) + 1
rib_count = int((body_length - rib_width) // rib_height) + 1
rib_count = int((body_length - rib_width) // rib_height) + 1
rib_profile = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(body_length)
)
inlet = (
    cq.Workplane("XY")
    .circle(inlet_radius)
    .extrude(inlet_radius)
)
inlet = rib_profile.extrude(body_length)
inlet = rib_profile.extrude(body_length)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_count)
    .translate((0, 0, body_length))
)
result = rib.union(rib)
result = result.edges("|Z").fillet(fillet_radius)
result = result.edges("|Z").chamfer(fillet_radius)
