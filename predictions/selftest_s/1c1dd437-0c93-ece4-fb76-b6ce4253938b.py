import cadquery as cq
outer_dia_big = 60.0
outer_dia_mid = 40.0
outer_dia_small = 20.0
length_big = 30.0
length_mid = 30.0
length_small = 30.0
through_hole_dia = 8.0
counterbore_dia = 12.0
counterbore_depth = 5.0
mount_hole_dia = 5.0
mount_pattern_radius = outer_dia_mid * 0.3
fillet_radius = 2.0
pocket_width = outer_dia_big * 0.4
pocket_height = outer_dia_big * 0.2
pocket_depth = length_big * 0.5
big = cq.Workplane('XY').circle(outer_dia_big/2).extrude(length_big)
mid = cq.Workplane('XY').circle(outer_dia_mid/2).extrude(length_mid).translate((0,0,length_big))
small = cq.Workplane('XY').circle(outer_dia_small/2).extrude(length_small).translate((0,0,length_big+length_mid))
result = big.union(mid).union(small)
result = result.edges().fillet(fillet_radius)
result = result.faces('>Z').workplane().hole(through_hole_dia)
result = result.faces('>Z').workplane().hole(counterbore_dia, counterbore_depth)
result = (result.workplane(offset=length_big + length_mid/2)
          .pushPoints([
              (mount_pattern_radius,0),
              (-mount_pattern_radius,0),
              (0,mount_pattern_radius),
              (0,-mount_pattern_radius)
          ])
          .hole(mount_hole_dia))
result = (result.faces('>X').workplane()
          .rect(pocket_width, pocket_height)
          .cutBlind(-pocket_depth))
