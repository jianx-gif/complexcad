import cadquery as cq

plate_length = 100.0
plate_width = 80.0
plate_thickness = 8.0
hole_diameter = 4.0
hole_rows = 4
hole_cols = 5
hole_spacing_x = 15.0
hole_spacing_y = 12.0
hole_offset_x = -30.0
hole_offset_y = -15.0
hole_depth = 5.0
emboss_radius = 10.0
emboss_height = 3.0
chamfer_size = 2.0
rib_thickness = 2.0
rib_width = 6.0
rib_spacing = 20.0

# Base plate creation
base_plate = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Central emboss
emboss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(emboss_radius)
    .extrude(emboss_height)
)

base_plate = base_plate.union(emboss)

# Blind hole pattern
hole_positions = []
for i in range(hole_rows):
    for j in range(hole_cols):
        x = hole_offset_x + j * hole_spacing_x
        y = hole_offset_y + i * hole_spacing_y
        hole_positions.append((x, y))

base_plate = (
    base_plate.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter, hole_depth)
)

# Edge chamfer on outer perimeter
base_plate = base_plate.edges().chamfer(chamfer_size)

# Add longitudinal ribs for stiffness
rib_start = -plate_length/2 + rib_spacing/2
rib_positions = []
while rib_start < plate_length/2:
    rib_positions.append(rib_start)
    rib_start += rib_spacing

for x_pos in rib_positions:
    rib = (
        cq.Workplane("YZ")
        .center(0, 0)
        .rect(rib_thickness, plate_width)
        .extrude(rib_width)
        .translate((x_pos, 0, plate_thickness/2))
    )
    base_plate = base_plate.union(rib)

result = base_plate
