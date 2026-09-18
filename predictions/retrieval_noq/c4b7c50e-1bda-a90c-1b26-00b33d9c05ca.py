import cadquery as cq

# Parameters
outer_size = 60.0
wall_thickness = 2.0
tube_length = 80.0
hole_diameter = 4.0
edge_clearance = 5.0
hole_rows = 3
hole_cols = 3
chamfer_distance = 1.0

# Derived dimensions
available_length = tube_length - 2 * edge_clearance
available_height = outer_size - 2 * edge_clearance
hole_spacing_z = available_length / (hole_rows - 1)
hole_spacing_y = available_height / (hole_cols - 1)

# Base solid: square tube
result = (
    cq.Workplane("XY")
    .rect(outer_size, outer_size)
    .extrude(tube_length)
    .shell(-wall_thickness)
    .edges("|Z or <Z or >Z")
    .chamfer(chamfer_distance)
)

# Drill hole grid on each outer side face
for outer_face in [">X", "<X", ">Y", "<Y"]:
    result = (
        result
        .faces(outer_face)
        .workplane(centerOption="CenterOfBoundBox")
        .rarray(hole_spacing_y, hole_spacing_z, hole_cols, hole_rows)
        .hole(hole_diameter)
    )
