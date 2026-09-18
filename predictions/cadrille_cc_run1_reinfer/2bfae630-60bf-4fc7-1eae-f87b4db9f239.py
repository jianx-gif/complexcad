import cadquery as cq
outer_diameter = 30.0
inner_diameter = 20.0
wall_thickness = 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius - wall_thickness
chamfer_distance = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(outer_radius, wall_thickness)
    .lineTo(outer_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().polarArray(radius=inner_radius - wall_thickness/2, count=4, startAngle=0, angle=360).hole(inner_radius * 2, angle=360).translate((0, 0, wall_thickness))
solid = solid
for i in range(1, 1):
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2)
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2, inner_radius * 2))
    solid = solid.faces(">Z").workplane().center(0, 0).hole(inner_radius * 2, inner_radius * 2, inner_radius * 2, inner_radius * 2))
result = solid
