import cadquery as cq

plate_length = 80.0
plate_width = 60.0
plate_thickness = 8.0
rib_width = 6.0
rib_height = 12.0
central_boss_dia = 20.0
central_boss_height = 20.0
oil_passage_dia = 8.0
clearance_hole_dia = 9.0
hole_offset = 30.0
chamfer_dist = 1.0

base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)

rib1 = cq.Workplane('XY').center(-plate_length/2 + rib_width/2, 0).rect(rib_width, plate_width).extrude(rib_height)

rib2 = cq.Workplane('XY').center(0, -plate_width/2 + rib_width/2).rect(plate_length, rib_width).extrude(rib_height)

ribs = rib1.union(rib2).translate((0, 0, plate_thickness - rib_height))

assembly = base.union(ribs)

boss = cq.Workplane('XY').center(0, 0).circle(central_boss_dia/2).extrude(central_boss_height).translate((0, 0, plate_thickness))
assembly = assembly.union(boss)

oil_hole = cq.Workplane('XY').center(0, 0).circle(oil_passage_dia/2).extrude(central_boss_height).translate((0, 0, plate_thickness))
assembly = assembly.cut(oil_hole)

for x in (-hole_offset, hole_offset):
    hole = cq.Workplane('XY').center(x, 0).circle(clearance_hole_dia/2).extrude(plate_thickness + 5)
    assembly = assembly.cut(hole)

result = assembly.edges("|Z").chamfer(chamfer_dist)
