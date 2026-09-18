import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 4.0
rib_height = 12.0
rib_width = 6.0
rib_length = 20.0
rib_count = 8
rib_count = 6
rib_count = 8
rib_radius = outer_diameter/2 - wall_thickness - rib_height/2
chamfer_size = 1.0
outer_radius = outer_diameter/2
inner_radius = inner_diameter/2
rib_radius = inner_radius + rib_height/2
rib_count = int((inner_radius - rib_radius) // rib_count)
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_diameter)
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .extrude(rib_height)
)
rib = (
    cq.Workplane("XY")
    .circle(rib_radius)
    .extrude(rib_height)
)
rib = rib.translate((rib_radius, 0, rib_height))
rib = rib.translate((rib_radius, 0, rib_height))
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_size)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
result = combined
