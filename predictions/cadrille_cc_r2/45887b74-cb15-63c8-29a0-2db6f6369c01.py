import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset_x = 15.0
hole_offset_y = 10.0
chamfer_distance = 0.5
base = cq.Workplane('XY').box(leg_length, leg_width, thickness)
base = base.faces('>Z').workplane().center(leg_length/2 - wall_thickness/2, leg_width/2 - wall_thickness/2).rect(rib_width, rib_height).extrude(thickness)
base = base.edges('|Z').chamfer(chamfer_distance)
rib = (cq.Workplane('XY')
       .box(rib_width, rib_height, thickness)
       .translate((leg_width/2 - wall_thickness/2, leg_width/2, thickness/2))
       .rotate((0,0,0), (0,0,1), 90)
       .translate((leg_width/2, leg_width/2, thickness/2)))
    base = base.union(rib)
result = base
