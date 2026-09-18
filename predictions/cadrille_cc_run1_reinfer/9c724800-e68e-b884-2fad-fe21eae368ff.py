import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 8.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_size = 1.0
base = cq.Workplane('XY').box(leg_length, leg_width, thickness)
base = base.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane('XY')
    .box(rib_width, leg_length, thickness)
    .translate((leg_width/2, leg_width/2, thickness/2))
)
base = base.union(rib)
base = base.edges('|Z').chamfer(chamfer_size)
base = base.edges('>Z').fillet(0.5)
base = base.faces('>Z').workplane().hole(hole_diameter)
base = base.faces('>Z').workplane().center(leg_width/2, leg_width/2).rect(leg_width, leg_length).extrude(thickness)
base = base.edges('>Z').chamfer(chamfer_size)
base = base.faces('>Z').workplane().center(leg_width/2, leg_width/2).rect(leg_width, leg_length).extrude(thickness)
base = base.edges('>Z').chamfer(chamfer_size)
result = base
