import cadquery as cq

hex_diameter = 80.0
arm_length = 100.0
groove_width = 5.0
groove_depth = 8.0
through_hole_diameter = 10.0
pivot_hole_diameter = 20.0
pivot_hole_offset = 15.0
chamfer_distance = 2.0
rib_width = 15.0
rib_height = 8.0
rib_length = 60.0
rib_offset = 20.0
notch_width = 12.0
notch_depth = 6.0
notch_offset = -20.0

result = (cq.Workplane("XY")
          .polygon(6, hex_diameter)
          .extrude(arm_length))

result = result.faces(">Z").workplane().hole(through_hole_diameter)

result = (result.faces("<Z").workplane()
          .center(pivot_hole_offset, 0)
          .hole(pivot_hole_diameter))

inner_hex_diameter = hex_diameter - 2 * groove_width

groove = (cq.Workplane("XY")
          .polygon(6, inner_hex_diameter)
          .extrude(groove_depth))

result = result.cut(groove)

rib = (result.faces(">Z").workplane()
       .center(rib_offset, 0)
       .rect(rib_width, rib_length)
       .extrude(rib_height))

result = result.union(rib)

notch = (result.faces(">Z").workplane()
        .center(notch_offset, 0)
        .rect(notch_width, arm_length/2)
        .cutBlind(notch_depth))

result = result.union(notch)

result = result.edges("|Z").chamfer(chamfer_distance)
