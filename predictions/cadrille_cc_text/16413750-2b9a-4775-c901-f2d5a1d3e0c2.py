import cadquery as cq
outer_radius = 30.0
top_radius = 20.0
base_height = 40.0
taper_height = 20.0
wall_thickness = 3.0
hole_diameter = 5.0
hole_depth = 15.0
hole_spacing = 12.0
hole_count = 6
chamfer_distance = 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, base_height)
    .lineTo(top_radius, base_height)
    .lineTo(top_radius, 0)
    .close()
)
base = profile.revolve()
base = base.edges().chamfer(chamfer_distance)
hole_cyl = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(hole_diameter / 2)
    .extrude(base_height + taper_height + 2)
)
base = base.cut(hole_cyl)
base = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=hole_count, startAngle=0, angle=360, count=hole_count)
    .circle(hole_diameter / 2)
    .cutBlind(hole_depth)
)
base = base.faces(">Z").edges().chamfer(chamfer_distance)
result = base
