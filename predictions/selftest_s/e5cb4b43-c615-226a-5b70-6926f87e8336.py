import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 80.0
plate_thickness = 5.0

dome_radius = 20.0
# Approximate dome height as a fraction of radius for a smooth cap
dome_height = dome_radius * 0.6

hole_diameter = 5.0
hole_grid_rows = 5
hole_grid_cols = 5
hole_grid_spacing_x = 15.0
hole_grid_spacing_y = 15.0

rim_chamfer = 1.0

mount_tab_length = 20.0
mount_tab_width = 10.0
mount_tab_thickness = 3.0
mount_tab_offset = 5.0

# Base plate centered at origin, thickness spans -plate_thickness/2 .. +plate_thickness/2
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Dome profile on XZ plane, revolve around Z axis
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(dome_radius, 0)
    .threePointArc((dome_radius, dome_height), (0, dome_height))
    .close()
)

dome = profile.revolve(360).translate((0, 0, plate_thickness/2))

# Combine base and dome
result = base.union(dome)

# Mounting tab definition (placed on +X side, centered in Y)
base_tab = (
    cq.Workplane("XY")
    .box(mount_tab_width, mount_tab_length, mount_tab_thickness)
    .translate((plate_length/2 - mount_tab_width/2 - mount_tab_offset,
                0,
                plate_thickness/2 + mount_tab_thickness/2))
)
# Add tab and three rotated copies
result = result.union(base_tab)
for angle in (90, 180, 270):
    rotated = base_tab.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.union(rotated)

# Compute ventilation hole centers, avoiding central dome region
hole_points = []
start_x = - (hole_grid_cols - 1) * hole_grid_spacing_x / 2
start_y = - (hole_grid_rows - 1) * hole_grid_spacing_y / 2
for i in range(hole_grid_cols):
    for j in range(hole_grid_rows):
        x = start_x + i * hole_grid_spacing_x
        y = start_y + j * hole_grid_spacing_y
        if (x**2 + y**2) > (dome_radius - hole_diameter)**2:
            hole_points.append((x, y))

# Drill holes from a workplane located at the top of the base plate (just below dome start)
result = result.workplane(offset=plate_thickness/2).pushPoints(hole_points).hole(hole_diameter)

# Add chamfer to all vertical edges (edges parallel to Z)
result = result.edges("|Z").chamfer(rim_chamfer)
