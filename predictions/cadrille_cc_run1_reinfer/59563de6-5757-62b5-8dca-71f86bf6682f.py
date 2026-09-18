import cadquery as cq
outer_diameter = 30.0
inner_diameter = 20.0
wall_thickness = 2.0
inner_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(wall_thickness)
)
inner = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(wall_thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(wall_thickness)
)
combined = base.union(rib)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.faces(">Z").edges().chamfer(chamfer_size)
combined = combined.faces("<Z").edges().chamfer(chamfer_size)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().hole(inner_radius * 2)
combined = combined.faces(">Z").workplane().polarArray(radius=inner_radius - wall_thickness/2, count=rib_spacing, startAngle=0, angle=360).hole(rib_width)
result = combined
