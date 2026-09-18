import cadquery as cq
outer_diameter = 80.0
wall_thickness = 3.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
fillet_radius = 1.0
chamfer_distance = 0.5
rib_width = 5.0
rib_height = 2.0
rib_thickness = 2.0
rib_spacing = 12.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, outer_diameter)
    .lineTo(inner_radius, outer_diameter)
    .lineTo(inner_radius, outer_diameter)
    .lineTo(inner_radius, outer_diameter)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness / 2.0, outer_diameter / 2.0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
