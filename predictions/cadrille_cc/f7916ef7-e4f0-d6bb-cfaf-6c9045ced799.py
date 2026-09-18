import cadquery as cq
leg_length = 80.0
leg_width = 20.0
thickness = 10.0
wall_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 12.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
rib_count = 4
base = cq.Workplane('XY').box(leg_width, leg_length, thickness)
base = base.edges().chamfer(chamfer_size)
base = base.faces('>Z').workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).extrude(rib_height)
base = base.faces('>Z').workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).extrude(rib_height)
base = base.faces('>Z').workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).extrude(rib_height)
base = base.faces('>Z').workplane().center(leg_length/2, leg_width/2).rect(rib_width, rib_height).cutBlind(-rib_height)
rib_count = int(leg_length // rib_spacing)
for i in range(rib_count):
    x = rib_spacing * i
    rib = rib.translate((x, leg_width/2 - rib_width/2, 0))
    rib = rib.translate((x, leg_width/2 - rib_width/2, 0))
    base = base.union(rib)
result = base
