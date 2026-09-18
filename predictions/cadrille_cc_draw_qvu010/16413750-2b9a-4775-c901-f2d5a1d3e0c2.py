import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
wall_thickness = 5.0
rib_height = 12.0
rib_width = 8.0
rib_thickness = 4.0
rib_count = 6
fillet_radius = 2.0
chamfer_distance = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter/2, 0)
    .lineTo(outer_diameter/2, 0)
    .lineTo(outer_diameter/2, rib_height)
    .lineTo(outer_diameter/2, rib_height)
    .lineTo(inner_diameter/2, rib_height)
    .lineTo(inner_diameter/2, rib_height)
    .lineTo(inner_diameter/2, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter/2)
    .extrude(rib_height)
    .translate((outer_diameter/2 - rib_thickness/2, 0, 0))
)
solid = solid.cut(rib)
solid = solid.faces(">Z").edges().fillet(fillet_radius)
result = solid
