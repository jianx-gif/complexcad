import cadquery as cq
outer_radius = 38
inner_radius = 15
wall_thickness = 2
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
chamfer_size = 1
hole_diameter = 5
hole_spacing = 12
hole_count = 6
hole_offset = 10
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, outer_radius)
    .lineTo(inner_radius + wall_thickness, outer_radius)
    .lineTo(inner_radius + wall_thickness, outer_radius)
    .lineTo(inner_radius, outer_radius)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_offset, count=hole_count, startAngle=0, angle=360).hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_offset, startAngle=0, angle=360, count=hole_count).hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_offset, count=hole_count, startAngle=0, angle=360).hole(hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=hole_offset, count=hole_count, startAngle=0, angle=360).hole(hole_diameter)
solid = solid.edges().chamfer(chamfer_size)
result = solid
