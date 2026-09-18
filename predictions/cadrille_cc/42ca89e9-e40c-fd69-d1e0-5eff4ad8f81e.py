import cadquery as cq
outer_diameter = 40.0
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
    .circle(outer_radius)
    .extrude(thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(inner_radius + wall_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(inner_radius + wall_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + wall_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
base = base.union(rib)
base = base.edges("|Z").fillet(fillet_radius)
result = base
