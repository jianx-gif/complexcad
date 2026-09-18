import cadquery as cq
outer_size = 40
wall_thickness = 2
conduit_length = 80
hole_diameter = 4
hole_spacing = 30
hole_count = 6
chamfer_size = 0.8
base = cq.Workplane('XY').box(outer_size, outer_size, conduit_length)
conduit = cq.Workplane('XY').box(conduit_length, conduit_length, conduit_length)
conduit = conduit.shell(-wall_thickness)
conduit = conduit.edges().chamfer(chamfer_size)
conduit = (
    conduit
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
conduit = (
    conduit
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
result = (
    conduit
    .edges('|Z')
    .chamfer(chamfer_size)
)
