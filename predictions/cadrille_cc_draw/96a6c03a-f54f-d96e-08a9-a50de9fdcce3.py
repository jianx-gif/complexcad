import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = 2.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_size = 0.5
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius + wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness)
    .lineTo(inner_radius + wall_thickness, wall_thickness + rib_height)
    .lineTo(inner_radius + wall_thickness, wall_thickness + rib_height)
    .lineTo(inner_radius, wall_thickness + rib_height)
    .lineTo(inner_radius, wall_thickness + rib_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .circle(rib_width)
    .extrude(rib_height)
    .translate((inner_radius + wall_thickness + rib_width/2, 0, wall_thickness + rib_height/2))
)
solid = solid.union(rib)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=inner_radius + wall_thickness/2, startAngle=0, count=4, angle=360)
    .hole(inner_radius * 2)
)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=inner_radius + wall_thickness/2, startAngle=0, angle=360, count=rib_count)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
solid = solid.union(rib)
solid = solid.edges().chamfer(chamfer_size)
result = solid
