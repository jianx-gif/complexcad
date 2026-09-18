import cadquery as cq

bore_radius = 10.0
wall_thickness = 5.0
start_outer_radius = bore_radius + wall_thickness
length = 80.0
end_width = 60.0
end_depth = 40.0
end_wall_thickness = 6.0
hole_diameter = 4.0
hole_rows = 3
hole_cols = 4
hole_spacing_x = (end_width - 2*end_wall_thickness) / (hole_cols + 1)
hole_spacing_y = (end_depth - 2*end_wall_thickness) / (hole_rows + 1)
chamfer_size = 1.0

housing = (
    cq.Workplane('XY')
    .circle(start_outer_radius)
    .workplane(offset=length)
    .rect(end_width, end_depth)
    .loft(combine=True)
)

bore = cq.Workplane('XY').cylinder(length, bore_radius).translate((0, 0, length/2))
housing = housing.cut(bore)

for i in range(1, hole_cols + 1):
    for j in range(1, hole_rows + 1):
        x = -end_width/2 + end_wall_thickness + i * hole_spacing_x
        y = -end_depth/2 + end_wall_thickness + j * hole_spacing_y
        housing = housing.faces('>Z').workplane().center(x, y).hole(hole_diameter)

housing = housing.faces('>Z').edges().chamfer(chamfer_size)

result = housing