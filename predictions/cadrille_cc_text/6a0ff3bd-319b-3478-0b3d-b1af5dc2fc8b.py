import cadquery as cq
total_length = 80.0
inlet_width = 50.0
inlet_height = 30.0
wall_thickness = 3.0
chamfer_size = 2.0
step_height = 5.0
step_width = 30.0
step_height = 20.0
rib_thickness = 2.0
rib_height = 12.0
rib_spacing = 10.0
base = cq.Workplane('XY').box(total_length, inlet_width, inlet_height)
shell = base.shell(-wall_thickness)
chamfered = shell.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane('XY')
    .rect(rib_thickness, rib_height)
    .rect(rib_thickness, rib_height)
    .loft()
)
result = chamfered.union(rib)
result = result.faces('>Z').workplane().rect(inlet_width, inlet_width).cutBlind(-wall_thickness)
result = result.faces('>Z').workplane().rect(inlet_width, inlet_width).cutBlind(-wall_thickness)
result = result.faces('>Z').workplane().rect(inlet_width, inlet_width).cutBlind(-wall_thickness)
