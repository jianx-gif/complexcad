import cadquery as cq

top_diameter = 80.0
base_diameter = 40.0
top_height = 5.0
mid_height = 15.0
base_height = 30.0
wall_thickness = 4.0
fillet_radius = 2.0
chamfer_distance = 1.5
screw_hole_dia = 5.0
screw_hole_spacing = 30.0
vent_slot_width = 4.0
vent_slot_height = 12.0
vent_slot_depth = wall_thickness * 2

base_radius = base_diameter/2
top_radius = top_diameter/2
mid_radius = (base_radius + top_radius)/2

profile = (cq.Workplane('XZ')
           .moveTo(0, 0)
           .lineTo(0, base_height - fillet_radius)
           .lineTo(base_radius, base_height - fillet_radius)
           .threePointArc((mid_radius, base_height), (mid_radius, base_height - fillet_radius))
           .lineTo(mid_radius, mid_height)
           .lineTo(top_radius, top_height)
           .lineTo(0, top_height)
           .close())
solid = profile.revolve(360)
result = solid.shell(-wall_thickness)
result = result.faces('<Z').edges().chamfer(chamfer_distance)
result = result.workplane(offset=top_height).pushPoints([(-screw_hole_spacing/2,0), (screw_hole_spacing/2,0)]).hole(screw_hole_dia)

num_vent = 6
for i in range(num_vent):
    angle = i * 360.0 / num_vent
    slot = (cq.Workplane('XZ')
            .rect(vent_slot_width, vent_slot_depth)
            .extrude(vent_slot_height)
            .rotate((0,0,0),(0,0,1), angle)
            .translate((mid_radius,0,mid_height)))
    result = result.cut(slot)
