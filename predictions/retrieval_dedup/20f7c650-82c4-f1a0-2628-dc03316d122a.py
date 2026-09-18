import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
fillet_radius = 5.0
hole_diameter = 15.0
hole_depth = 8.0
wp = cq.Workplane("XY")
wp = wp.moveTo(0, 0)
wp = wp.lineTo(leg_width - fillet_radius, 0)
wp = wp.radiusArc((leg_width, fillet_radius), fillet_radius)
wp = wp.lineTo(leg_width, leg_length - thickness - fillet_radius)
wp = wp.radiusArc((leg_width - fillet_radius, leg_length - thickness), fillet_radius)
wp = wp.lineTo(leg_width - thickness, leg_length - thickness)
wp = wp.lineTo(leg_width - thickness, leg_length)
wp = wp.lineTo(fillet_radius, leg_length)
wp = wp.radiusArc((0, leg_length - fillet_radius), fillet_radius)
wp = wp.close()
result = wp.extrude(thickness)
# central blind hole on longer leg
result = result.faces(">Z").workplane().center(leg_width/2, leg_length/2).circle(hole_diameter/2).cutBlind(-hole_depth)
# reinforcing rib on short leg
result = result.faces(">Z").workplane().center(leg_width/4, leg_length/2).rect(leg_width/2, thickness/2).cutBlind(-5)
# rib on long leg
result = result.faces(">Z").workplane().center(leg_width*3/4, leg_length/2).rect(thickness/2, leg_length/2).cutBlind(-5)
