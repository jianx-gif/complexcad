import cadquery as cq
panel_length = 80
panel_width = 60
panel_thickness = 4
fillet_radius = 0.5
hole_diameter = 2
blind_hole_depth = panel_thickness - 0.5
tab_width = 30
tab_height = 8
slot_width = 2
slot_length = 12

base = cq.Workplane("XY").box(panel_length, panel_width, panel_thickness)

tab = (
    cq.Workplane("XY")
    .center(panel_length/2 - tab_width/2, 0)
    .rect(tab_width, tab_height)
    .extrude(panel_thickness)
)
panel = base.union(tab)
panel = panel.edges("|Z").fillet(fillet_radius)

panel = (
    panel
    .faces(">Z")
    .workplane()
    .circle(hole_diameter/2)
    .cutBlind(blind_hole_depth)
)

panel = (
    panel
    .faces(">Z")
    .workplane()
    .polarArray(count=6, radius=15, startAngle=0, angle=360)
    .circle(hole_diameter/2)
    .cutBlind(blind_hole_depth)
)

panel = (
    panel
    .faces(">Z")
    .workplane()
    .center(0, -panel_width/2 + slot_width/2)
    .rarray(xSpacing=20, ySpacing=0, xCount=3, yCount=1)
    .rect(slot_length, slot_width)
    .cutBlind(blind_hole_depth)
)
result = panel