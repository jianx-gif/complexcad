import cadquery as cq

# Primary dimensions (max 100 units)
total_height = 80.0
spine_width = 20.0
spine_thickness = 10.0
base_width = 90.0
base_thickness = 15.0
steps = 8
step_height = total_height / steps
lattice_pitch = 12.0
lattice_bar_thickness = 2.0
chamfer_distance = 0.5

# Initialize thin base plate
prev_width = spine_width
prev_thick = spine_thickness
core = cq.Workplane("XY").rect(prev_width, prev_thick).extrude(0.01)

for i in range(1, steps + 1):
    new_width = spine_width + (base_width - spine_width) * (i / steps)
    new_thick = spine_thickness + (base_thickness - spine_thickness) * (i / steps)
    core = (
        core.faces(">Z")
        .workplane(offset=0)
        .rect(prev_width, prev_thick)
        .workplane(offset=step_height)
        .rect(new_width, new_thick)
        .loft(combine=True)
    )
    prev_width = new_width
    prev_thick = new_thick

# Chamfer top perimeter edges for safety
core = core.faces(">Z").edges().chamfer(chamfer_distance)

# Lattice pattern: X and Y oriented bars using pushPoints grid
grid_count = int(base_width / lattice_pitch) + 2
half_steps = grid_count // 2
points = [(i * lattice_pitch, j * lattice_pitch) for i in range(-half_steps, half_steps + 1) for j in range(-half_steps, half_steps + 1)]

bars_x = (
    cq.Workplane("XY")
    .pushPoints(points)
    .rect(lattice_pitch - lattice_bar_thickness, lattice_bar_thickness)
    .extrude(total_height)
)

bars_y = (
    cq.Workplane("XY")
    .pushPoints(points)
    .rect(lattice_bar_thickness, lattice_pitch - lattice_bar_thickness)
    .extrude(total_height)
)

lattice = bars_x.union(bars_y)

result = core.cut(lattice)
