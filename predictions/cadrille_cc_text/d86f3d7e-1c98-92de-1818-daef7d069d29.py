import cadquery as cq
outer_radius = 30.0
inner_radius = 25.0
height = 60.0
ridge_radial_thickness = 2.0
ridge_height = 6.0
chamfer_dist = 3.0
hole_diameter = 6.0
hole_count = 6
hole_spacing = (outer_radius - inner_radius) / 2.0
hole_spacing = (outer_radius - inner_radius) / 2.0
hole_positions = [(hole_spacing * (hole_count - 1) / 2.0, hole_spacing * (hole_spacing * (hole_count - 1) / 2.0), hole_spacing * (hole_spacing * (hole_count - 1) / 2.0)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(outer_radius + ridge_radial_thickness, height)
    .lineTo(outer_radius + ridge_radial_thickness, ridge_height)
    .lineTo(outer_radius, ridge_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_dist)
hole_positions = [(-hole_spacing/2, 0), (hole_spacing/2, 0)]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
result = (
    solid.faces(">Z")
    .workplane()
    .circle(hole_diameter/2)
    .extrude(ridge_height)
)
