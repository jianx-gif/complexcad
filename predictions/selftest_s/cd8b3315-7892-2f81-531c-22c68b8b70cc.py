import cadquery as cq
spacer_length = 80.0
spacer_width = 50.0
spacer_height = 12.0
wall_thickness = 4.0
rib_thickness = 2.0
rib_spacing = 15.0
rib_height = spacer_height - wall_thickness*2
tab_width = 10.0
tab_height = 5.0
tab_length = 30.0
detent_gap = 2.0
chamfer_distance = 0.8
outer = cq.Workplane('XY').box(spacer_length, spacer_width, spacer_height, centered=(True, True, False)).edges('|Z').chamfer(chamfer_distance)
inner_width = spacer_width - 2*wall_thickness
inner_length = spacer_length - 2*wall_thickness
inner = cq.Workplane('XY', (0,0,wall_thickness)).box(inner_length, inner_width, spacer_height - wall_thickness, centered=(True, True, False))
base = outer.cut(inner)
inner_width_half = inner_width/2.0
positions = []
pos = -inner_width_half + rib_thickness/2.0
while pos <= inner_width_half - rib_thickness/2.0:
    positions.append(pos)
    pos += rib_thickness + rib_spacing
spaced = base.faces('>Z').workplane().pushPoints([(x,0) for x in positions])
spaced = spaced.rect(rib_thickness, spacer_length - 2*wall_thickness).cutBlind(-rib_height)
# peripheral detent tab
tab = cq.Workplane('YZ', (spacer_length/2.0,0,wall_thickness)).box(tab_length, tab_width, tab_height, centered=(True, False, False))
# cut a small gap for detent
gap = cq.Workplane('YZ', (spacer_length/2.0 - tab_length + detent_gap,0,wall_thickness)).box(detent_gap, tab_width, tab_height, centered=(True, False, False))
tab = tab.cut(gap)
result = spaced.union(tab)
