import cadquery as cq
inner_radius = 15.0
wall_thickness = 5.0
clip_length = 60.0
knurl_cylinder_dia = 2.0
knurl_depth = 0.8
relief_hole_dia = 8.0
relief_hole_offset = 30.0
chamfer_distance = 1.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, clip_length - knurl_depth)
    .lineTo(inner_radius + knurl_depth, clip_length - knurl_depth)
    .lineTo(inner_radius + knurl_depth, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
hole_positions = [
    (inner_radius, 0),
    (inner_radius, clip_length - knurl_depth),
    (inner_radius + knurl_depth, clip_length - knurl_depth),
    (inner_radius + knurl_depth, 0),
]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .circle(relief_hole_dia / 2)
    .cutBlind(-relief_hole_offset)
)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=inner_radius + knurl_depth/2, startAngle=0, angle=360, count=relief_hole_offset)
    .circle(knurl_cylinder_dia/2)
    .cutBlind(-knurl_depth)
)
result = solid
