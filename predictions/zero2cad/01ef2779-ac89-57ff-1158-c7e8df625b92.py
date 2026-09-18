import cadquery as cq

# Parameters
length = 80.0
outer_width = 40.0
outer_height = 30.0
wall_thickness = 5.0
inner_width = outer_width - 2 * wall_thickness
inner_height = outer_height - 2 * wall_thickness
rib_width = 6.0
rib_height = 12.0
rib_spacing = 12.0
rib_count = int((length - 2 * wall_thickness) // rib_spacing)
chamfer_size = 1.0

# Base solid: outer block
outer = cq.Workplane("XY").rect(outer_width, outer_height).extrude(length)
# Inner cavity cut
inner = cq.Workplane("XY").rect(inner_width, inner_height).extrude(length)
base = outer.cut(inner)
# Rib profile (centered on XY plane)
rib_profile = cq.Workplane("XY").rect(rib_width, rib_height).extrude(wall_thickness)
# Position ribs on +X side, spaced along length
ribs = cq.Workplane("XY")
for i in range(rib_count):
    z_pos = wall_thickness + i * rib_spacing
    rib = rib_profile.translate((outer_width/2 - wall_thickness/2, 0, z_pos))
    ribs = ribs.union(rib)
# Combine base and ribs
result = base.union(ribs)
# Chamfer top edges for safety
result = result.faces(">Z").edges().chamfer(chamfer_size)
