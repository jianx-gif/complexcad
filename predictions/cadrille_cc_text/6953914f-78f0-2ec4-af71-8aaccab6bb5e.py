import cadquery as cq
outer_diameter = 70.0
length = 30.0
wall_thickness = 2.0
central_hole_diameter = 12.0
central_hole_radius = outer_diameter / 2.0
diameter = outer_diameter / 2.0
dimple_depth = 1.5
chamfer_distance = 0.8
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(length)
    .faces(">Z")
    .workplane()
    .circle(central_hole_radius)
    .cutBlind(-length)
)
inner_radius = outer_diameter / 2.0 - chamfer_distance
inner_radius = inner_radius + wall_thickness
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(length)
    .translate((0, 0, length))
)
result = base.cut(inner_cyl)
result = result.edges().chamfer(chamfer_distance)
result = result.edges().chamfer(chamfer_distance)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius=inner_radius + wall_thickness / 2.0, count=4, startAngle=0, angle=360)
    .hole(dimple_depth)
)
