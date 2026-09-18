import cadquery as cq

length = 100.0
leg_width = 30.0
wall_thickness = 4.0
fillet_radius = 6.0
chamfer_dist = 1.0
hole_dia = 10.0
hole_depth = 20.0
hole_offset = 15.0

leg1 = (cq.Workplane('YZ')
        .rect(leg_width, leg_width)
        .extrude(length)
        .shell(-wall_thickness))

leg2 = (cq.Workplane('XZ')
        .rect(leg_width, leg_width)
        .extrude(length)
        .shell(-wall_thickness))

corner = leg1.union(leg2)
corner = corner.edges("|Z and (<X or <Y)").fillet(fillet_radius)
corner = corner.edges(">X or >Y or >Z").chamfer(chamfer_dist)

hole_center_y = leg_width/2 - wall_thickness - hole_dia/2
result = (corner.faces('>X')
          .workplane()
          .center(hole_center_y, 0)
          .circle(hole_dia/2)
          .cutBlind(-hole_depth))