import cadquery as cq

# Parameters
foot_diameter = 60.0            # Diameter across opposite vertices of hex foot
foot_height = 5.0               # Thickness of hex foot
total_height = 80.0             # Overall height of part (including foot)
section_count = 8               # Number of loft steps after foot
reduction_factor = 0.7          # Scale factor for radius each step
initial_radius = foot_diameter / 2.0
final_radius = 2.0              # Small radius at tip
section_height = (total_height - foot_height) / section_count
chamfer_size = 0.5

# Hole pattern parameters
hole_diameter = 4.0
hole_depth = 15.0               # Blind hole depth
hole_rows = 4
hole_cols = 4
hole_spacing_x = foot_diameter * 0.6 / (hole_cols - 1)
hole_spacing_y = foot_diameter * 0.6 / (hole_rows - 1)
mid_section_index = section_count // 2
mid_section_z = foot_height + mid_section_index * section_height

# Helper for radius at a given step
def radius_at_step(step):
    if step == 0:
        return initial_radius
    radius = initial_radius * (reduction_factor ** step)
    return max(radius, final_radius)

# Create hexagonal foot
result = cq.Workplane("XY").polygon(6, foot_diameter).extrude(foot_height)

# Incrementally loft circular sections up to tip
solid = result
for i in range(1, section_count + 1):
    r_start = radius_at_step(i - 1)
    r_end = radius_at_step(i)
    solid = (
        solid
        .faces('>Z')
        .circle(r_start)
        .workplane()
        .transformed(offset=(0, 0, section_height))
        .circle(r_end)
        .loft(combine=True)
    )

# Chamfer all edges for safety
solid = solid.edges().chamfer(chamfer_size)

# Patterned blind holes at mid height, drilled inward
hole_grid = []
start_x = - (hole_cols - 1) * hole_spacing_x / 2
start_y = - (hole_rows - 1) * hole_spacing_y / 2
for ix in range(hole_cols):
    for iy in range(hole_rows):
        hole_grid.append((start_x + ix * hole_spacing_x, start_y + iy * hole_spacing_y))

solid = solid.workplane(offset=mid_section_z, invert=True).pushPoints(hole_grid).hole(hole_diameter, hole_depth)

result = solid
