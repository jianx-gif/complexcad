import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
spacer_height = 12.0
rib_thickness = 5.0
rib_width = 6.0
rib_height = spacer_height * 0.6
mounting_hole_diameter = 15.0
mounting_hole_offset = 5.0
chamfer_distance = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter/2, 0)
    .lineTo(inner_diameter/2, spacer_height)
    .lineTo(inner_diameter/2 + rib_thickness, spacer_height)
    .lineTo(inner_diameter/2 + rib_thickness, spacer_height + rib_height)
    .lineTo(inner_diameter/2, spacer_height + rib_height)
    .lineTo(inner_diameter/2, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(inner_diameter/2 + rib_thickness/2, 0)
    .box(rib_width, rib_thickness, rib_height)
)
solid = solid.union(rib)
solid = solid.edges().chamfer(chamfer_distance)
result = solid
