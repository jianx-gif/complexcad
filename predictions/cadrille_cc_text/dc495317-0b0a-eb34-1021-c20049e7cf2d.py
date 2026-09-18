import cadquery as cq
rod_length = 80.0
step_height = 40.0
step_height = step_height - 2.0
shell_thk = 2.0
shell_thk = 3.0
edge_chamfer = 0.5
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(rod_length, 0)
    .lineTo(rod_length, rod_length - shell_thk)
    .threePointArc((rod_length - shell_thk, rod_length), (rod_length - shell_thk, rod_length))
    .lineTo(rod_length, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(edge_chamfer)
solid = solid.faces(">Z").workplane().hole(plate_hole_diameter)
solid = solid.faces(">Z").workplane().hole(plate_hole_diameter)
solid = solid.faces(">Z").workplane().pushPoints([(0,0),(0,0),(0,1), 1), 24])
solid = solid.faces(">Z").workplane().pushPoints([(0,0),(0,0),(0,1), 1), 24)).circle(2).cutBlind(-shell_thk)
result = solid
