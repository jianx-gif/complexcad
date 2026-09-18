import cadquery as cq

# Parameters
plate_length = 90
plate_width = 70
plate_thickness = 5
fillet_radius = 3
hole_diameter = 6
hole_spacing_x = 50
hole_spacing_y = 40
boss_base_radius = 15
boss_top_radius = 10
boss_height = 15
boss_extra_height = 2
rib_height = 2
rib_thickness = 2
rib_spacing = 20

# Base plate solid
plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Fillet outer perimeter
plate = plate.edges("|Z").fillet(fillet_radius)

# Mounting holes (rectangular 4-hole pattern)
hole_offset_x = (plate_length - hole_spacing_x) / 2
hole_offset_y = (plate_width - hole_spacing_y) / 2
hole_positions = [
    (-hole_offset_x, -hole_offset_y),
    (hole_offset_x, -hole_offset_y),
    (-hole_offset_x, hole_offset_y),
    (hole_offset_x, hole_offset_y),
]
plate = (
    plate.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Stiffening ribs on underside (grid pattern)
num_ribs_x = int((plate_length - 2 * rib_thickness) // rib_spacing) + 1
num_ribs_y = int((plate_width - 2 * rib_thickness) // rib_spacing) + 1
rib_points = []
for i in range(num_ribs_x):
    for j in range(num_ribs_y):
        x = -plate_length/2 + rib_thickness + i * rib_spacing
        y = -plate_width/2 + rib_thickness + j * rib_spacing
        rib_points.append((x, y))

ribs = (
    cq.Workplane("XY")
    .pushPoints(rib_points)
    .rect(rib_thickness, rib_thickness)
    .extrude(-rib_height)
)

plate = plate.union(ribs)

# Central boss via revolve
profile_points = [
    (0, plate_thickness),
    (boss_base_radius, plate_thickness),
    (boss_base_radius, plate_thickness + boss_height),
    (boss_top_radius, plate_thickness + boss_height + boss_extra_height),
    (0, plate_thickness + boss_height + boss_extra_height),
]

boss = (
    cq.Workplane("XZ")
    .polyline(profile_points)
    .close()
    .revolve()
)

# Combine plate and boss
result = plate.union(boss)
