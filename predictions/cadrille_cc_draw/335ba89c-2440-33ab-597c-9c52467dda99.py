import cadquery as cq
arm_length = 80.0
arm_width = 30.0
arm_thickness = 8.0
arm_height = 20.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 20.0
hole_spacing_y = 15.0
chamfer_size = 0.5
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (arm_length, 0),
        (arm_length, arm_width),
        (arm_length - rib_width, arm_width),
        (arm_length - rib_width, arm_width + rib_height),
        (arm_length - rib_width, arm_width + rib_height),
        (arm_length, arm_width + rib_height),
        (arm_length, 0),
    ])
    .close()
    .extrude(arm_thickness)
)
rib = (
    base.faces(">Z").workplane()
    .center(0, arm_width/2)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
result = base.union(rib)
hole_positions = [
    (hole_cols - 1) * hole_spacing_x,
    (hole_rows - 1) * hole_spacing_y,
    (hole_rows - 1) * hole_spacing_y,
]
for i in range(hole_cols):
    for j in range(hole_rows):
        x = hole_spacing_x + i * hole_spacing_x
        y = hole_spacing_y + j * hole_spacing_y
        hole_positions.append((x, y))
result = (
    result.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
