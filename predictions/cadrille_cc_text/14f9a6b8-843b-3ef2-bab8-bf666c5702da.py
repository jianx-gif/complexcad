import cadquery as cq
hub_radius = 20.0
bracket_length = 25.0
bracket_height = 12.0
tip_relief_length = 5.0
tip_relief_width = 6.0
tip_relief_depth = 1.5
tip_relief_depth = 2.0
chamfer_size = 0.5
hole_diameter = 3.0
hole_count = 4
hole_spacing = (hub_radius - 2 * lip_relief_length) / (hole_count - 1)
base = (
    cq.Workplane("XY")
    .moveTo(hub_radius, 0)
    .lineTo(hub_radius, hub_radius)
    .lineTo(bracket_length, hub_radius)
    .lineTo(bracket_length, 0)
    .close()
    .revolve()
)
tip_body = base.faces(">Z").workplane().hole(hole_diameter)
tip_body = tip_body.edges().fillet(tip_relief_depth)
tip_relief = (
    cq.Workplane("XY")
    .center(hub_radius - tip_relief_depth/2, 0)
    .rect(tip_relief_width, tip_relief_depth)
    .extrude(tip_relief_depth)
)
tip_relief = tip_relief.cut(tip_relief)
result = base.union(tip_relief)
result = result.faces(">Z").edges().fillet(chamfer_size)
