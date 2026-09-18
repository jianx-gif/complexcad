import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 80.0
rib_height = 40.0
rib_width = 6.0
rib_thickness = 4.0
rib_count = 6
chamfer_size = 1.0
hole_diameter = 4.0
hole_depth = thickness / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter/2, 0)
    .lineTo(inner_diameter/2, thickness)
    .lineTo(outer_diameter/2, thickness)
    .lineTo(outer_diameter/2, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter/2, thickness + rib_height/2)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
solid = solid.cut(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
