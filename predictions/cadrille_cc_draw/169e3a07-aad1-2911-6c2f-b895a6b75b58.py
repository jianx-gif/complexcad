import cadquery as cq
outer_diameter = 70
inner_diameter = 30
wall_thickness = 5
inner_radius = inner_diameter / 2
rib_thickness = 2
rib_height = 4
rib_count = 6
chamfer_size = 1
mount_hole_dia = 5
mount_hole_offset = 10
mount_hole_count = 4
mount_hole_radius = outer_diameter / 2 - wall_thickness
outer_radius = outer_diameter / 2
inner_radius = inner_radius + wall_thickness
inner_radius = inner_radius + wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(rib_height)
)
rib = rib.edges().chamfer(chamfer_size)
rib = (
    rib.faces(">Z")
    .workplane()
    .circle(inner_radius)
    .extrude(rib_height)
)
rib = rib.edges().chamfer(chamfer_size)
rib = (
    rib.faces(">Z")
    .workplane()
    .rect(rib_thickness, rib_height)
    .extrude(rib_height)
)
rib = rib.edges(">Z").chamfer(chamfer_size)
result = rib
