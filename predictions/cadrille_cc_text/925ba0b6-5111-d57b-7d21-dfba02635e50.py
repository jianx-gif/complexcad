import cadquery as cq
clip_height = 30.0
arm_height = 30.0
flange_radius = 12.0
flange_thickness = 4.0
chamfer = 0.6
cbore_diameter = 5.5
cbore_depth = 2.5
width = 6.0
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, arm_height)
    .lineTo(flange_radius, arm_height)
    .lineTo(flange_radius, flange_thickness)
    .lineTo(0, flange_thickness)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer)
solid = (
    solid.faces(">Z")
    .workplane()
    .center(0, flange_thickness/2)
    .rect(width, flange_thickness)
    .cutBlind(-flange_thickness)
)
solid = solid.edges().chamfer(chamfer)
result = solid
