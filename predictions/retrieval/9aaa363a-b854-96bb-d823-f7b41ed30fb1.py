import cadquery as cq
plate_length = 80
plate_width = 60
plate_thickness = 6
chamfer_size = 4
pocket_length = 40
pocket_width = 30
pocket_depth = 3
hole_diameter = 4
hole_depth = 5
hole_spacing = 20
hole_count = 3
hole_offset = 12
rib_thickness = 2
rib_width = 10
rib_depth = 2
base = cq.Workplane('XY').rect(plate_length, plate_width).extrude(plate_thickness)
base = base.edges('|Z').chamfer(chamfer_size)
base = base.faces('>Z').workplane().rect(pocket_length, pocket_width).cutBlind(pocket_depth)
hole_points = [(hole_offset + i*hole_spacing, hole_offset) for i in range(hole_count)]
base = base.faces('>Z').workplane().pushPoints(hole_points).hole(hole_diameter, hole_depth)
rib1 = cq.Workplane('XY').rect(plate_length - 2*hole_offset, rib_width).extrude(rib_thickness)
rib1 = rib1.translate((0, -plate_width/2 + rib_width/2 + hole_offset, -plate_thickness/2 + rib_thickness/2))
rib2 = rib1.mirror(mirrorPlane='YZ')
result = base.union(rib1).union(rib2)