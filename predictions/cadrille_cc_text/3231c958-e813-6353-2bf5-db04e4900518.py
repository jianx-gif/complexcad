import cadquery as cq
outer_radius = 45.0
inner_radius = 20.0
thickness = 10.0
blind_hole_diameter = 8.0
blind_hole_depth = 7.0
outer_chamfer = 2.0
inner_chamfer = 1.0
rib_width = 3.0
rib_height = 8.0
rib_thickness = 2.0
mounting_hole_diameter = 5.0
mounting_hole_offset = 5.0
base = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius + rib_thickness, thickness)
    .lineTo(inner_radius + rib_thickness, thickness + rib_height)
    .lineTo(inner_radius + rib_thickness, thickness + rib_height)
    .lineTo(inner_radius, thickness + rib_height)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)
base = base.faces(">Z").edges().chamfer(outer_chamfer)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness/2, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
    .translate((inner_radius + rib_thickness/2, 0, thickness + rib_height/2))
)
base = base.union(rib)
base = base.edges("|Z").chamfer(outer_chamfer)
base = base.faces(">Z").edges().chamfer(outer_chamfer)
base = base.faces(">Z").edges().chamfer(outer_chamfer)
result = base
