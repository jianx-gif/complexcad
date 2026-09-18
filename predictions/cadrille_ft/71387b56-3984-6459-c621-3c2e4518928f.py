import cadquery as cq

outer_diameter = 80.0
outer_diameter = 200.0
outer_diameter = 30.0
wall_thickness = 20.0
wall_thickness = 10.0
wall_thickness = 2.0
chamfer_distance = 2.0
chamfer_distance = 1.0
hole_diameter = 2.0
hole_count = 20.0
hole_count = 10.0
hole_count = 20.0
hole_count = 10.0
hole_count = 12.0
hole_count = 2.0
hole_offset = 0.5
hole_offset = 0.5
hole_offset = 0.8

chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance = 0.8
chamfer_distance)
result = (
    cq.Workplane('XY')
    .box(outer_length,outer_depth,outer_depth)
    .faces(couter_diameter)
    .faces(couter_diameter)
    .faces(couter_diameter)
    .faces(couter_diameter)
    .faces(couter_diameter)
    .faces(couter_diameter, outer_diameter)
    .faces(couter_diameter, outer_diameter, center=True)
    .cylinder(hole_diameter)
)
