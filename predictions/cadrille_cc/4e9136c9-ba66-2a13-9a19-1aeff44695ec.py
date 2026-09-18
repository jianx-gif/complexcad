import cadquery as cq
outer_radius = 40.0
inner_radius = 20.0
height = 30.0
wall_thickness = 2.0
fillet_radius = 1.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_offset = 15.0
chamfer_distance = 0.5
profile = (
    cq.Workplane("XY")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().fillet(fillet_radius)
solid = solid.edges().fillet(fillet_radius)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter, depth=hole_offset).hole(hole_diameter, depth=hole_offset)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter, depth=hole_offset).hole(hole_diameter, depth=hole_offset)
solid = solid.faces(">Z").workplane().center(0, 0).hole(hole_diameter, depth=hole_offset).cutBlind(-hole_depth)
solid = solid.faces(">Z").workplane().center(hole_offset, 0).hole(hole_diameter, depth=hole_offset).hole(hole_diameter, depth=hole_offset)
solid = solid.faces("<Z").workplane().center(hole_offset, 0).hole(hole_diameter, depth=hole_offset).hole(hole_diameter, depth=hole_offset).edges().fillet(fillet_radius)
result = solid
