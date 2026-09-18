import cadquery as cq
import math
outer_diameter = 80.0
overall_length = 50.0
wall_thickness = 8.0
inner_diameter = outer_diameter - 2 * wall_thickness
keyway_width = 6.0
keyway_depth = wall_thickness - 2.0
clearance_hole_diameter = 5.0
chamfer_distance = 2.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
keyway_length = overall_length
hole_radius = clearance_hole_diameter / 2.0
hole_length = wall_thickness + 2.0
# Base outer cylinder
outer_cyl = cq.Workplane('XY').circle(outer_radius).extrude(overall_length)
# Inner bore
inner_cyl = cq.Workplane('XY').circle(inner_radius).extrude(overall_length)
# Housing after bore
housing = outer_cyl.cut(inner_cyl)
# Keyway cut (rectangular slot)
keyway_box = (
    cq.Workplane('XY')
    .center(outer_radius - keyway_depth / 2.0, 0)
    .box(keyway_depth, keyway_width, keyway_length, centered=(True, True, False))
)
housing = housing.cut(keyway_box)
# Clearance holes around circumference (4 equally spaced)
angles = [0, 90, 180, 270]
radial_center = inner_radius + wall_thickness / 2.0
for ang in angles:
    rad = math.radians(ang)
    x_off = radial_center * math.cos(rad)
    y_off = radial_center * math.sin(rad)
    hole = (
        cq.Workplane('YZ')
        .center(0, 0)
        .circle(hole_radius)
        .extrude(hole_length)
        .rotate((0, 0, 0), (0, 0, 1), ang)
        .translate((x_off, y_off, 0))
    )
    housing = housing.cut(hole)
# Chamfer outer edges (vertical edges on outer cylinder)
result = housing.edges("|Z").chamfer(chamfer_distance)
