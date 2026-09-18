import cadquery as cq
total_height = 60.0
base_radius = 10.0
wall_thickness = 4.0
fillet_radius = 1.0
hole_diameter = 6.0
hole_count = 8
hole_spacing = total_height / 2.0
hole_pattern_radius = total_height / 2.0
hole_pattern_count = 4
chamfer_distance = 0.5
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, total_height - fillet_radius)
    .threePointArc((base_radius + fillet_radius, total_height), (0, total_height))
    .close()
)
solid = profile.revolve()
solid = solid.shell(-wall_thickness)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
hole_cyl = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(hole_diameter / 2.0)
    .extrude(hole_pattern_radius * 2)
)
solid = solid.cut(hole_cyl)
solid = solid.faces(">Z").edges().fillet(fillet_radius)
result = solid
