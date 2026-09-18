import cadquery as cq
total_height = 50.0
base_outer_radius = 30.0
shoulder_height = 8.0
shoulder_outer_radius = 20.0
central_bore_diameter = 12.0
countersink_hole_diameter = 6.0
countersink_csk_diameter = 10.0
countersink_angle = 82.0
countersink_spacing = 30.0
top_chamfer = 0.8
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_outer_radius, 0)
    .lineTo(base_outer_radius, shoulder_height - shoulder_height)
    .lineTo(shoulder_outer_radius, shoulder_height - shoulder_height)
    .lineTo(shoulder_outer_radius, shoulder_height)
    .lineTo(0, shoulder_height)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(top_chamfer)
solid = solid.faces(">Z").workplane().hole(central_bore_diameter)
solid = solid.faces(">Z").workplane().hole(countersink_hole_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=total_height/2, count=4, startAngle=0, angle=360).hole(countersink_csk_diameter)
solid = solid.faces(">Z").workplane().polarArray(radius=total_height/2, count=4, startAngle=0, angle=360).cskHole(countersink_csk_diameter, countersink_csk_diameter, countersink_angle)
solid = solid.faces(">Z").workplane().polarArray(radius=total_height/2, count=4, angle=360).cskHole(countersink_hole_diameter, countersink_csk_diameter, countersink_angle)
result = solid
