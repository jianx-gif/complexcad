import cadquery as cq
outer_radius = 12.0
inner_radius = 10.0
wall_thickness = 2.0
fillet_radius = 1.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_count = 4
hole_spacing = 12.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 15.0
hole_spacing_y = 12.0
profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(outer_radius, wall_thickness + fillet_radius)
    .lineTo(inner_radius, wall_thickness + fillet_radius)
    .lineTo(inner_radius, wall_thickness + fillet_radius)
    .lineTo(inner_radius, wall_thickness + fillet_radius)
    .lineTo(inner_radius, wall_thickness + fillet_radius)
    .lineTo(inner_radius, wall_thickness + fillet_radius)
    .lineTo(inner_radius, wall_thickness + fillet_radius)
    .lineTo(inner_radius, wall_thickness + fillet_radius)
    .lineTo(inner_radius, wall_thickness + fillet_radius)
    .lineTo(inner_radius, wall_thickness + fillet_radius)
    .lineTo(inner_radius, wall_thickness + fillet_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces("<Z").edges().fillet(fillet_radius)
solid = solid.faces("<Z").edges().fillet(fillet_radius)
solid = solid.faces("<Z").edges().fillet(fillet_radius)
result = solid
