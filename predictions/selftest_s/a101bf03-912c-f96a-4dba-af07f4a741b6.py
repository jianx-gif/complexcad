import cadquery as cq

# Parameters
inlet_radius = 18.0
wall_thickness = 3.0
outlet_radius = 8.0
conduit_length = 60.0
taper_length = 20.0
flange_thickness = 5.0
flange_outer_radius = 30.0
mount_hole_diameter = 4.0
mount_hole_offset = 10.0
mount_hole_count = 4
chamfer_size = 0.8
boss_thickness = 4.0
boss_width = 8.0
boss_height = 6.0

# Derived dimensions
total_height = flange_thickness + conduit_length + taper_length

# Outer profile sketch in XY plane
outer_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(inlet_radius, 0)
    .vLine(flange_thickness)
    .hLine(flange_outer_radius - inlet_radius)
    .vLine(conduit_length)
    .lineTo(outlet_radius, total_height)
    .lineTo(0, total_height)
    .close()
)

# Revolve to create solid
outer_solid = outer_profile.revolve(360, (0, 0, 0), (0, 0, 1))

# Shell to create thin wall
hollow = outer_solid.shell(wall_thickness)

# Through hole to open both ends
through_hole = (
    cq.Workplane("XY")
    .cylinder(height=total_height * 1.2, radius=outlet_radius - wall_thickness)
    .translate((0, 0, -total_height * 0.1))
)
part_open = hollow.cut(through_hole)

# Chamfer outer edge
part_chamfered = part_open.edges().chamfer(chamfer_size)

# Mounting holes on top flange
part_with_holes = (
    part_chamfered.faces(">Z").workplane()
    .rarray(mount_hole_offset, mount_hole_offset, mount_hole_count, mount_hole_count)
    .hole(mount_hole_diameter)
)

# Side boss protrusion intersecting wall, placed within flange region
boss = (
    cq.Workplane("XY")
    .box(boss_thickness, boss_width, boss_height)
    .translate((flange_outer_radius - boss_thickness / 2, 0, flange_thickness / 2))
)

result = part_with_holes.union(boss)
