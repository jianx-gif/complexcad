import cadquery as cq
base_diameter = 70.0
base_height = 30.0
shoulder_diameter = 50.0
shoulder_height = 15.0
shell_thickness = 4.0
edge_chamfer = 2.0
pilot_hole_diameter = 5.0
pilot_hole_count = 4
pilot_hole_radius = base_diameter / 2.0
outer_radius = base_diameter / 2.0
inner_radius = outer_radius - shoulder_diameter
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, base_height)
    .lineTo(shoulder_diameter / 2.0, base_height)
    .lineTo(shoulder_diameter / 2.0, base_height)
    .lineTo(0, base_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(edge_chamfer)
solid = solid.faces(">Z").workplane().hole(pilot_hole_diameter)
solid = solid.faces(">Z").workplane().hole(pilot_hole_diameter)
solid = solid.faces(">Z").workplane().hole(pilot_hole_diameter)
solid = solid.faces(">Z").edges().chamfer(edge_chamfer)
result = solid
