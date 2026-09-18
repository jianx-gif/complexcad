import cadquery as cq
outer_radius = 30.0
wall_thickness = 5.0
guide_length = 80.0
guide_radius = outer_radius - wall_thickness
guide_radius = outer_radius - guide_length
rib_thickness = 2.0
rib_height = 8.0
rib_base_height = 30.0
mounting_hole_diameter = 4.0
mounting_hole_spacing = 20.0
mounting_hole_count = 4
mounting_hole_radius = mounting_hole_diameter / 2.0
chamfer_size = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, guide_length)
    .lineTo(0, guide_length)
    .lineTo(0, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(mounting_hole_diameter)
solid = solid.faces(">Z").workplane().hole(mounting_hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(mounting_hole_spacing, 0, 360, mounting_hole_count).hole(mounting_hole_diameter)
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_base_height)
)
solid = solid.union(rib)
result = solid
