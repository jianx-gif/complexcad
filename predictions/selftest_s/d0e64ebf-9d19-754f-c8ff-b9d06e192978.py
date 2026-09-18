import cadquery as cq

body_diameter = 80.0
body_height = 60.0
wall_thickness = 5.0
bore_diameter = 30.0
groove_width = 2.0
groove_depth = 4.0
groove_position = 25.0
vent_hole_diameter = 8.0
vent_hole_offset_z = 30.0
fillet_radius = 0.5
lug_width = 12.0
lug_height = 6.0
lug_thickness = 4.0

body_radius = body_diameter / 2.0
bore_radius = bore_diameter / 2.0
groove_outer_radius = bore_radius + groove_width

# Base cylinder
base = cq.Workplane("XY").circle(body_radius).extrude(body_height)
# Fillet top and bottom edges
base = base.faces(">Z").edges().fillet(fillet_radius)
base = base.faces("<Z").edges().fillet(fillet_radius)
# Central bore
base = base.faces("<Z").workplane().hole(bore_diameter, depth=body_height)
# O‑ring groove (ring‑shaped pocket)
outer = cq.Workplane("XY").circle(groove_outer_radius).extrude(groove_depth).translate((0,0,groove_position))
inner = cq.Workplane("XY").circle(bore_radius).extrude(groove_depth+2).translate((0,0,groove_position-1))
base = base.cut(outer.cut(inner))
# Side vent hole
vent = cq.Workplane("YZ").circle(vent_hole_diameter/2).extrude(body_diameter+2).translate((0, vent_hole_offset_z, body_radius))
base = base.cut(vent)
# Mounting lugs on opposite sides (intrude into body for solid fusion)
lug_profile = cq.Workplane("YZ").rect(lug_thickness, lug_height).extrude(lug_width)
# Position lugs so they intersect the body by half their thickness
lug1 = lug_profile.translate((0, body_radius - lug_thickness/2, body_height/2))
lug2 = lug_profile.translate((0, -(body_radius - lug_thickness/2), body_height/2))
base = base.union(lug1).union(lug2)
result = base
