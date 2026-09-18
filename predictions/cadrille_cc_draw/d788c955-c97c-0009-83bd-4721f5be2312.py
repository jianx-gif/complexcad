import cadquery as cq
outer_radius = 10.0
inner_radius = 20.0
wall_thickness = 2.0
rib_height = 50.0
rib_thickness = 4.0
rib_spacing = 12.0
rib_count = 6
rib_count = 8
chamfer_size = 0.5
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius + rib_thickness, outer_radius)
    .lineTo(inner_radius + rib_thickness, rib_height)
    .lineTo(inner_radius + rib_thickness, rib_height)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness/2, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_thickness)
)
rib = rib.edges().chamfer(chamfer_size)
rib = rib.faces(">Z").workplane().hole(inner_radius * 2)
rib = rib.faces(">Z").workplane().hole(inner_radius * 2)
rib = rib.faces(">Z").workplane().center(0, 0).rect(rib_thickness, rib_height).extrude(rib_thickness)
rib = rib.faces(">Z").workplane().center(0, 0).rect(rib_thickness, rib_height).cutBlind(-rib_thickness)
rib = rib.edges("|Z").chamfer(chamfer_size)
result = rib
