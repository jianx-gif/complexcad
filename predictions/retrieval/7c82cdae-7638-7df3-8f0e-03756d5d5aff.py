
import cadquery as cq

# Dimensions (max 100 units)
horizontal_leg_length = 80.0
vertical_leg_length = 70.0
leg_thickness = 15.0
bracket_depth = 10.0
rib_width = 4.0
rib_depth = 6.0
rib_height = 5.0
rib_count = 3
hole_diameter = 6.0
hole_spacing = 20.0
chamfer_size = 1.0

# L‑profile points for 2D sketch
profile_pts = [
    (0, 0),
    (horizontal_leg_length, 0),
    (horizontal_leg_length, leg_thickness),
    (leg_thickness, leg_thickness),
    (leg_thickness, vertical_leg_length),
    (0, vertical_leg_length),
    (0, 0)
]

# Base L‑bracket solid
bracket = (
    cq.Workplane("XY")
    .polyline(profile_pts)
    .close()
    .extrude(bracket_depth)
)

# Rib reinforcement (grid of small rectangular ribs on top of inner corner)
spacing_x = (leg_thickness - rib_width) / (rib_count + 1)
spacing_y = (leg_thickness - rib_depth) / (rib_count + 1)

rib_template = cq.Workplane().box(rib_width, rib_depth, rib_height)

ribs_combined = None
for i in range(rib_count):
    for j in range(rib_count):
        x_center = spacing_x * (i + 1) + rib_width / 2
        y_center = spacing_y * (j + 1) + rib_depth / 2
        z_center = bracket_depth + rib_height / 2
        rib_instance = rib_template.translate((x_center, y_center, z_center))
        ribs_combined = rib_instance if ribs_combined is None else ribs_combined.union(rib_instance)

bracket = bracket.union(ribs_combined)

# Clearance holes on vertical arm (front -Y face) – 2×2 grid
hole_grid = (
    bracket
    .faces("<Y")
    .workplane()
    .center(leg_thickness/2 - hole_spacing/2, vertical_leg_length/2 - hole_spacing/2)
    .rarray(hole_spacing, hole_spacing, 2, 2)
    .hole(hole_diameter)
)

bracket = hole_grid

# Chamfer outer edges for safety
bracket = bracket.edges("|Z").chamfer(chamfer_size)

result = bracket
