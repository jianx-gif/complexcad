import cadquery as cq

# Parameters
outer_radius = 40.0
wall_thickness = 3.0
inner_radius = outer_radius - wall_thickness
cap_height = 30.0
rib_height = 5.0
rib_width = 2.0
rib_outer_radius = outer_radius + rib_width
rib_start_height = cap_height - rib_height
hole_diameter = 3.0
hole_count = 8
hole_offset_height = cap_height * 0.6
chamfer_distance = 0.5
extra_cut_depth = 0.2

# Create outer profile and revolve to form cap shell
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, rib_start_height)
    .lineTo(rib_outer_radius, rib_start_height)
    .lineTo(rib_outer_radius, cap_height)
    .lineTo(0, cap_height)
    .close()
)

# Revolve profile around Z axis
cap_outer = outer_profile.revolve()

# Shell to create wall thickness
cap_shell = cap_outer.shell(-wall_thickness)

# Chamfer top rim edges for safety
cap_chamfered = cap_shell.faces(">Z").edges().chamfer(chamfer_distance)

# Patterned holes using polar array on sketch before extrude
hole = (
    cq.Workplane("XZ")
    .center(outer_radius - wall_thickness/2, hole_offset_height)
    .circle(hole_diameter/2)
    .polarArray(count=hole_count, startAngle=0, angle=360, radius=0)
    .extrude(wall_thickness + extra_cut_depth)
)

# Cut holes through side wall
result = cap_chamfered.cut(hole)

# Internal reinforcement ribs (two orthogonal ribs inside the cap)
inner_rib_width = 4.0
inner_rib_height = cap_height - rib_height - 2.0
rib1 = (
    cq.Workplane("XY")
    .rect(inner_rib_width, inner_rib_height)
    .extrude(wall_thickness - 0.5)
    .translate((0, 0, rib_start_height + 1))
)

rib2 = rib1.rotate((0, 0, 0), (0, 0, 1), 90)

result = result.union(rib1).union(rib2)

# Add a small reinforcing boss on top interior
boss_radius = 6.0
boss_height = 3.0
boss = (
    cq.Workplane("XY")
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, cap_height - boss_height - 0.5))
)

result = result.union(boss)
