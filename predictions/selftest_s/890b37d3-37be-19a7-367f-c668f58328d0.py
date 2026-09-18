import cadquery as cq
panel_width = 100
panel_height = 80
panel_thickness = 4
border_chamfer = 2
slot_length = 20
slot_width = 4
slot_spacing = 12
num_slots = 5
hole_diameter = 6
hole_spacing = 20
num_hole_rows = 3

result = cq.Workplane("XY").rect(panel_width, panel_height).extrude(panel_thickness)
result = result.edges("|Z").chamfer(border_chamfer)

start_y = panel_height/2 - 15
for i in range(num_slots):
    result = (result.faces(">Z")
                  .workplane()
                  .center(0, start_y - i*slot_spacing)
                  .slot2D(slot_length, slot_width)
                  .cutBlind(-panel_thickness))

result = (result.faces(">Z")
              .workplane()
              .center(0,0)
              .rect(30,15)
              .cutBlind(-panel_thickness/2))

for row in range(num_hole_rows):
    y = -panel_height/2 + 20 + row*hole_spacing
    points = []
    for col in range(4):
        x = -panel_width/2 + 20 + col*hole_spacing
        points.append((x,y))
    result = (result.faces(">Z")
                  .workplane()
                  .pushPoints(points)
                  .hole(hole_diameter))
