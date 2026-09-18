import cadquery as cq
outer_diameter = 80.0
wall_thickness = 4.0
length = 60.0
inlet_center_offset = 30.0
inlet_center = length - 2 * wall_thickness
inlet_center = length / 2.0
inlet_chamfer = 2.0
rib_thickness = 2.0
rib_height = 10.0
rib_spacing = 15.0
rib_count = 4
rib_spacing = 15.0
rib_count = 3
rib_offset = (length - 2 * wall_thickness) / rib_spacing
outer_radius = outer_diameter / 2.0
inlet_center = length / 2.0
inlet_center = length / 2.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, length)
    .lineTo(inlet_center, length)
    .lineTo(inlet_center, length)
    .lineTo(0, length)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(inlet_chamfer)
rib = (
    cq.Workplane("XY")
    .center(rib_offset, rib_spacing)
    .rect(rib_thickness, rib_height)
    .extrude(length)
    .translate((rib_offset, rib_spacing, 0))
)
solid = solid.union(rib)
result = solid
