import cadquery as cq
total_length = 80.0
start_width = 45.0
total_depth = 20.0
wall_thickness = 3.0
fillet_radius = 1.0
groove_width = 30.0
groove_depth = 5.0
groove_width = 15.0
groove_depth = wall_thickness
fillet_radius = 1.0
base = (
    cq.Workplane("XY")
    .rect(start_width, start_width)
    .loft()
    .workplane(offset=total_depth)
    .rect(groove_width, groove_depth)
    .loft(combine=True)
)
hollow = base.shell(-wall_thickness)
filleted = hollow.edges("|Z").fillet(fillet_radius)
groove_cut = (
    filleted.faces(">Z")
    .workplane()
    .rect(groove_width, groove_depth)
    .cutBlind(-groove_depth)
)
hollow = filleted.faces(">Z").edges().chamfer(fillet_radius)
result = hollow
