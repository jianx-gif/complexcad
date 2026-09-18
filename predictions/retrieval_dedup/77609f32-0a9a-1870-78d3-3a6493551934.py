import cadquery as cq

# Parameters
num_teeth = 120
pitch = 0.8
tooth_height = 10.0
back_thickness = 5.0
gear_depth = 8.0
chamfer_distance = 0.3
bracket_width = 6.0
bracket_height = 4.0
bracket_thickness = 3.0
bracket_hole_dia = 2.0
bracket_spacing_teeth = 15

# Derived dimensions
total_length = num_teeth * pitch
bracket_spacing = pitch * bracket_spacing_teeth
bracket_count = int(num_teeth / bracket_spacing_teeth)

# Build rack profile points
points = []
points.append((0, 0))
points.append((0, back_thickness))
for i in range(num_teeth):
    x0 = i * pitch
    x1 = (i + 1) * pitch
    apex_x = x0 + pitch / 2.0
    points.append((apex_x, back_thickness + tooth_height))
    points.append((x1, back_thickness))
points.append((total_length, 0))

rack = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(gear_depth)
    .edges("|Z")
    .chamfer(chamfer_distance)
)

brackets_pattern = (
    rack.faces("<Z")
    .workplane()
    .rect(bracket_width, bracket_height)
    .extrude(-bracket_thickness)
    .rarray(bracket_spacing, 0, bracket_count, 1)
    .hole(bracket_hole_dia)
)

result = rack.union(brackets_pattern)
