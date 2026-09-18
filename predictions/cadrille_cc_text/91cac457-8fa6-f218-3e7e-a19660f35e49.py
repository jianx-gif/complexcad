import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
plate_thickness = 8.0
central_hole_diameter = 20.0
fillet_radius = 2.0
rib_width = 6.0
rib_height = 3.0
rib_count = 12
rib_spacing = (outer_diameter - inner_diameter) / 2.0
slot_width = 4.0
slot_depth = 2.0
slot_depth_z = 4.0
slot_count = 4
slot_offset = (outer_diameter - inner_diameter) / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_diameter / 2.0, 0)
    .lineTo(outer_diameter / 2.0, plate_thickness)
    .lineTo(inner_diameter / 2.0, plate_thickness)
    .lineTo(inner_diameter / 2.0, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").workplane().hole(central_hole_diameter)
solid = solid.faces(">Z").workplane().hole(central_hole_diameter)
slot = (
    cq.Workplane("XY")
    .box(slot_width, slot_depth, slot_depth_z)
    .translate((outer_diameter / 2.0 - slot_depth / 2.0, 0, slot_depth_z))
)
solid = solid.cut(slot)
boss = (
    cq.Workplane("XY")
    .box(boss_height, boss_diameter, plate_thickness)
    .translate((outer_diameter / 2.0 - boss_height / 2.0, 0, slot_depth_z))
)
solid = solid.union(boss)
result = solid
