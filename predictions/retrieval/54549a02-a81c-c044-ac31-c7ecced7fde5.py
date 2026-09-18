import cadquery as cq

bracket_length = 60.0
bracket_width = 30.0
bracket_thickness = 8.0
slot_length = bracket_length - 20.0
slot_height = 6.0
slot_depth = 6.0
lip_height = 12.0
lip_thickness = 3.0
rib_count = 4
rib_width = 4.0
rib_thickness = 2.0
rib_height = 5.0
counterbore_dia = 10.0
counterbore_depth = 4.0
through_hole_dia = 5.0
through_hole_spacing = 20.0
chamfer_size = 0.5

result = (cq.Workplane("XY")
          .rect(bracket_length, bracket_width)
          .extrude(bracket_thickness))

result = (result
          .faces("<Y")
          .workplane()
          .rect(slot_length, slot_height)
          .cutBlind(slot_depth))

result = (result
          .faces(">X")
          .workplane()
          .rect(lip_height, lip_thickness)
          .extrude(lip_thickness))

result = (result
          .faces(">Z")
          .workplane()
          .circle(counterbore_dia/2)
          .cutBlind(counterbore_depth)
          .circle(through_hole_dia/2)
          .cutBlind(bracket_thickness))

hole_count = int(bracket_length/through_hole_spacing)
result = (result
          .faces(">Z")
          .workplane()
          .rarray(through_hole_spacing, 0, hole_count, 1)
          .hole(through_hole_dia))

rib_spacing = (bracket_length - rib_count * rib_width) / (rib_count + 1)
rib_points = []
for i in range(rib_count):
    x_pos = -bracket_length/2 + rib_spacing * (i + 1) + rib_width * i + rib_width/2
    rib_points.append((x_pos, 0))

ribs = (cq.Workplane("XY")
        .pushPoints(rib_points)
        .rect(rib_width, rib_height)
        .extrude(-rib_thickness))
result = result.union(ribs)

result = result.faces(">Z").edges().chamfer(chamfer_size)
