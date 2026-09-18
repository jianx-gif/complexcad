import cadquery as cq
import math
plate_length = 80
plate_width = 50
plate_thickness = 8
rib_width = 6
rib_height = 4
rib_spacing = 12
rib_margin = 10
chamfer_distance = 1
bolt_hole_diameter = 5
bolt_hole_spacing = 30
pocket_width = 20
pocket_height = 10
pocket_depth = 4
rib_count = int(math.floor((plate_length - 2 * rib_margin) / rib_spacing)) + 1
base_plate = (cq.Workplane("XY")
    .rect(plate_width, plate_length)
    .extrude(plate_thickness))
rib_pattern = (base_plate.faces("<Z").workplane()
    .rect(rib_width, plate_thickness)
    .rarray(rib_spacing, 0, rib_count, 1, center=True)
    .extrude(-rib_height))
result = base_plate.union(rib_pattern)
result = result.edges("|Z").chamfer(chamfer_distance)
result = (result.faces(">Z").workplane()
    .pushPoints([(-bolt_hole_spacing/2, 0), (bolt_hole_spacing/2, 0)])
    .hole(bolt_hole_diameter))
result = (result.faces(">Z").workplane()
    .center(0, plate_width/2 - pocket_width/2)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth))
tab_thickness = 3
tab_length = 12
left_tab = (result.faces("<X").workplane()
    .center(0, 0)
    .rect(tab_thickness, plate_width)
    .extrude(tab_length))
right_tab = (result.faces(">X").workplane()
    .center(0, 0)
    .rect(tab_thickness, plate_width)
    .extrude(-tab_length))
result = result.union(left_tab).union(right_tab)
