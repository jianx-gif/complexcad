import cadquery as cq

leaf_length = 80.0
leaf_width = 30.0
leaf_thickness = 5.0
tip_radius = 6.0
clip_slot_width = 1.5
clip_slot_height = 40.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_rows = 3
hole_columns = 5
pin_diameter = 6.0
pin_depth = 3.0
fillet_radius = 0.8
chamfer_distance = 0.5

outer = (
    cq.Workplane("XY")
    .moveTo(-leaf_width/2, 0)
    .lineTo(-leaf_width/2, leaf_length)
    .lineTo(0, leaf_length + tip_radius)
    .lineTo(leaf_width/2, leaf_length)
    .lineTo(leaf_width/2, 0)
    .close()
    .wire()
)

leaf = outer.extrude(leaf_thickness)
leaf = leaf.edges("|Z").fillet(fillet_radius)

leaf = (
    leaf.faces(">Z").workplane()
    .center(0, leaf_length*0.3)
    .rect(clip_slot_width, clip_slot_height)
    .cutBlind(-leaf_thickness)
)

leaf = (
    leaf.faces(">Z").workplane()
    .center(0, leaf_length*0.75)
    .circle(pin_diameter/2)
    .cutBlind(-pin_depth)
)

points = []
start_x = -leaf_width/2 + hole_spacing
start_y = leaf_thickness + hole_spacing
for i in range(hole_columns):
    for j in range(hole_rows):
        x = start_x + i*hole_spacing
        y = start_y + j*hole_spacing
        points.append((x, y))
leaf = (
    leaf.faces(">Z").workplane()
    .pushPoints(points)
    .hole(hole_diameter)
)

leaf = leaf.edges("|Y").chamfer(chamfer_distance)

result = leaf