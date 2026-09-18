import cadquery as cq
outer_radius = 30.0
block_length = 50.0
block_length = block_length * 0.6
clearance_slot_width = 10.0
clearance_slot_depth = 12.0
clearance_slot_count = 8
mount_hole_diameter = 5.0
mount_hole_offset = 18.0
rib_width = 8.0
rib_thickness = 3.0
rib_height = 6.0
rib_count = 4
outer_radius = outer_radius - block_length / 2.0
inner_radius = outer_radius - block_length / 2.0
base = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, block_length)
    .lineTo(outer_radius, block_length + rib_height)
    .lineTo(outer_radius, 0)
    .close()
)
base = base.cut(inner_radius)
base = base.edges().fillet(fillet_radius)
base = base.faces(">Z").workplane().hole(mount_hole_diameter)
base = base.faces(">Z").workplane().hole(mount_hole_diameter)
base = base.faces(">Z").workplane().hole(mount_hole_diameter)
base = base.faces(">Z").workplane().polarArray(radius=mount_hole_offset, count=clearance_slot_count, startAngle=0, angle=360).hole(mount_hole_diameter)
base = base.faces(">Z").workplane().hole(mount_hole_diameter)
base = base.faces(">Z").workplane().polarArray(radius=mount_hole_offset, count=clearance_slot_count, startAngle=0, angle=360).hole(mount_hole_diameter)
base = base.faces(">Z").workplane().polarArray(radius=outer_radius - clearance_slot_depth/2, count=clearance_slot_count, startAngle=0, angle=360).hole(mount_hole_diameter)
base = base.faces(">Z").edges().fillet(rib_count)
result = base
