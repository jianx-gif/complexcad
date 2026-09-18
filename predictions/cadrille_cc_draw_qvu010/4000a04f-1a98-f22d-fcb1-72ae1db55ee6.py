import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 5.0
rib_height = 12.0
rib_width = 10.0
rib_thickness = 2.0
rib_count = 6
rib_count = 4
rib_radius = inner_diameter/2 - wall_thickness - rib_thickness/2
rib_count = 4
rib_spacing = 15.0
chamfer_distance = 1.0
outer_radius = outer_diameter/2
inner_radius = inner_diameter/2
base = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, outer_diameter)
    .lineTo(outer_radius, outer_diameter)
    .lineTo(outer_radius, outer_diameter - rib_height)
    .lineTo(outer_radius, outer_diameter - rib_height)
    .lineTo(outer_radius, 0)
    .close()
    .revolve()
)
rib = (
    cq.Workplane("XY")
    .box(rib_width, rib_thickness, rib_height)
    .translate((outer_radius - rib_thickness/2, 0, rib_count))
)
combined = base.union(rib)
combined = combined.edges().chamfer(chamfer_distance)
combined = combined.faces(">Z").workplane().hole(inner_diameter)
combined = combined.faces(">Z").workplane().polarArray(radius=inner_radius - rib_thickness/2, count=rib_count, startAngle=0, angle=360).hole(rib_radius)
result = combined
