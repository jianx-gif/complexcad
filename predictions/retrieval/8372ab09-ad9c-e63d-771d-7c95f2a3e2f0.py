import cadquery as cq
leg_length=80
leg_thickness=10
depth=20
horizontal=cq.Workplane('XY').rect(leg_length,leg_thickness).translate((leg_length/2,-leg_thickness/2,0)).extrude(depth)
vertical=cq.Workplane('XY').rect(leg_thickness,leg_length).translate((-leg_thickness/2,leg_length/2,0)).extrude(depth)
result=horizontal.union(vertical)
