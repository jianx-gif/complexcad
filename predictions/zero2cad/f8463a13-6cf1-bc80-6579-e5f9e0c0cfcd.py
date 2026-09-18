import cadquery as cq

# Parameters
outer_radius = 30.0
wall_thickness = 4.0
inner_radius_base = outer_radius - wall_thickness
inner_radius_top = inner_radius_base - 6.0
height = 60.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_depth = 12.0
hole_count = 8
hole_radius = outer_radius - wall_thickness/2
boss_radius = 6.0
boss_height = 8.0
boss_offset_angle = 45.0

# Base profile for revolve (XZ plane)
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius_top, height)
    .lineTo(inner_radius_base, 0)
    .close()
)

# Revolve to create hollow conical bracket
bracket = profile.revolve()

# Chamfer outer edges
bracket = bracket.edges().chamfer(chamfer_size)

# Add a cylindrical boss on the outer surface at a specific angle
boss = (
    cq.Workplane("XY")
    .center(outer_radius - wall_thickness/2, 0)
    .circle(boss_radius)
    .extrude(boss_height)
    .rotate((0, 0, 0), (0, 0, 1), boss_offset_angle)
)
bracket = bracket.union(boss)

# Create blind holes pattern on outer cylindrical face
holes = (
    cq.Workplane("XY")
    .polarArray(radius=hole_radius, startAngle=0, angle=360, count=hole_count)
    .circle(hole_diameter/2)
    .extrude(-hole_depth)
)
bracket = bracket.cut(holes)

result = bracket