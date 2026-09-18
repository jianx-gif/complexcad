import cadquery as cq
pipe_outer_radius = 5.0
pipe_thickness = 1.0
gusset_thickness = 2.0
gusset_width = 15.0
gusset_length = 30.0
chamfer_distance = 0.3
hole_diameter = 2.0
fillet_radius = 0.5
base = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(pipe_outer_radius, 0)
    .lineTo(pipe_outer_radius, pipe_thickness)
    .lineTo(gusset_thickness, pipe_thickness)
    .lineTo(gusset_thickness, pipe_thickness + gusset_width)
    .lineTo(gusset_thickness + gusset_width, pipe_thickness + gusset_length)
    .lineTo(gusset_thickness, pipe_thickness)
    .lineTo(gusset_thickness, pipe_thickness)
    .close()
    .extrude(gusset_length)
)
result = base.union(base)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .circle(hole_diameter / 2)
    .extrude(gusset_length)
)
result = (
    result.faces(">Z").workplane()
    .center(0, 0)
    .circle(gusset_thickness / 2)
    .extrude(gusset_length)
)
result = result.edges("|Z").chamfer(chamfer_distance)
