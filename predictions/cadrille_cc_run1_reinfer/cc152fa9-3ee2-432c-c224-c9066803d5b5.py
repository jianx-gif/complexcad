import cadquery as cq
outer_radius = 45.0
inner_radius = 30.0
wall_thickness = 2.0
inner_radius = inner_radius - wall_thickness
chamfer_distance = 0.5
rib_width = 5.0
rib_height = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 6
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, wall_thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = outer_profile.revolve()
solid = solid.edges().chamfer(chamfer_distance)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().hole(inner_radius * 2)
solid = solid.faces(">Z").workplane().circle(inner_radius).extrude(wall_thickness)
solid = solid.faces(">Z").workplane().circle(inner_radius).extrude(wall_thickness)
solid = solid.faces(">Z").workplane().circle(inner_radius).extrude(wall_thickness)
solid = solid.faces(">Z").workplane().circle(inner_radius).extrude(wall_thickness)
solid = solid.faces(">Z").workplane().circle(inner_radius).extrude(wall_thickness)
solid = solid.faces(">Z").workplane().circle(inner_radius).extrude(wall_thickness)
solid = solid.faces(">Z").workplane().circle(inner_radius).extrude(wall_thickness)
solid = solid.faces(">Z").workplane().circle(inner_radius).extrude(wall_thickness)
solid = solid.faces(">Z").workplane().circle(inner_radius).extrude(wall_thickness)
solid = solid.faces(">Z").workplane().polarArray(radius=inner_radius - wall_thickness/2, count=rib_count, startAngle=0, angle=360).hole(rib_width)
result = solid
