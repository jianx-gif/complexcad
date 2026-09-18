import cadquery as cq

outer_radius = 40.0
inner_radius = 15.0
retainer_thickness = 12.0
bore_diameter = 8.0
fillet_radius = 1.5
chamfer_distance = 1.0
slot_width = 4.0
slot_depth = outer_radius - inner_radius - 4.0
num_slots = 6
set_screw_hole_dia = 3.0
set_screw_depth = 5.0
set_screw_offset_angle = 30.0

profile = (
    cq.Workplane("XY")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, retainer_thickness)
    .lineTo(outer_radius, retainer_thickness)
    .lineTo(outer_radius, 0)
    .close()
)

solid = profile.revolve()

central_bore = cq.Workplane("XY").circle(bore_diameter / 2).extrude(retainer_thickness)
solid = solid.cut(central_bore)

solid = solid.faces(">X").edges().chamfer(chamfer_distance)
solid = solid.faces("<X").edges().fillet(fillet_radius)

slot_radius = inner_radius + (outer_radius - inner_radius) / 2
solid = (
    solid.faces(">Z").first().workplane()
    .polarArray(radius=slot_radius, startAngle=0, count=num_slots, angle=360)
    .rect(slot_width, slot_depth)
    .cutBlind(-slot_depth)
)

set_screw = (
    cq.Workplane("XY")
    .circle(set_screw_hole_dia / 2)
    .extrude(set_screw_depth)
    .rotate((0, 0, 0), (0, 0, 1), set_screw_offset_angle)
    .translate((slot_radius, 0, retainer_thickness / 2))
)
solid = solid.cut(set_screw)

result = solid