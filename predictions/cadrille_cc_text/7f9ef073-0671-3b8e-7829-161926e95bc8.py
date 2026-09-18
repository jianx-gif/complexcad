import cadquery as cq
bore_diameter = 30.0
outer_diameter = 60.0
collar_width = 20.0
groove_depth = 2.0
groove_width = 5.0
groove_offset = 4.0
tab_width = 10.0
tab_thickness = 3.0
tab_height = 4.0
slot_width = 5.0
slot_length = 15.0
slot_depth = 3.0
rib_width = 2.0
rib_thickness = 2.0
rib_height = 4.0
base = cq.Workplane('XY').circle(outer_diameter/2).extrude(collar_width)
base = base.faces('>Z').workplane().hole(outer_diameter)
base = base.faces('>Z').workplane().hole(outer_diameter)
base = base.faces('>Z').workplane().polarArray(radius=outer_diameter/2 - tab_thickness/2, count=slot_width/2, startAngle=0, angle=360).rect(slot_width, slot_length).cutBlind(-groove_depth)
base = base.faces('>Z').workplane().polarArray(radius=outer_diameter/2 - tab_thickness/2, startAngle=0, angle=360).rect(tab_width, tab_thickness).extrude(tab_height)
base = base.union(base)
base = base.faces('>Z').workplane().polarArray(radius=outer_diameter/2 - tab_thickness/2, count=slot_width/2, startAngle=0, angle=360).rect(slot_width, slot_length).extrude(tab_height)
base = base.union(base)
base = base.faces('>Z').workplane().polarArray(radius=outer_diameter/2 - tab_thickness/2, count=slot_width/2, startAngle=0, angle=360).rect(tab_width, tab_thickness).extrude(tab_height)
base = base.union(base)
base = base.faces('>Z').workplane().polarArray(radius=outer_diameter/2 - tab_thickness/2, count=slot_width/2, startAngle=0, angle=360).rect(tab_width, tab_thickness).extrude(tab_height)
base = base.faces('>Z').workplane().polarArray(radius=outer_diameter/2 - tab_thickness/2, count=slot_width/2, angle=360).rect(tab_width, tab_thickness).extrude(tab_height)
base = base.union(base)
base = base.faces('>Z').edges().fillet(fillet_radius)
base = base.faces('>Z').edges().chamfer(0.5)
base = base.faces('>Z').edges().fillet(fillet_radius)
base = base.faces('>Z').workplane().center(bore_diameter/2 - tab_thickness/2, 0).hole(bore_diameter)
base = base.faces('>Z').workplane().center(bore_diameter/2 - tab_thickness/2, 0).rect(tab_width, tab_thickness).extrude(tab_height)
base = base.faces('>Z').workplane().center(bore_diameter/2 - tab_thickness/2, 0).rect(tab_width, tab_thickness).extrude(tab_height)
base = base.union(base)
base = base.faces('>Z').edges().chamfer(fillet_radius)
result = base
