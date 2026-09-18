import cadquery as cq
flange_length=80.0
flange_width=60.0
flange_thickness=6.0
rib_thickness=4.0
rib_height=8.0
plate=cq.Workplane('XY').rect(flange_length,flange_width).extrude(flange_thickness)
# ribs
top_rib=plate.faces('>Z').workplane().center(0,flange_width/2 - rib_thickness/2).rect(flange_length-2*rib_thickness, rib_thickness).extrude(rib_height)
bottom_rib=plate.faces('>Z').workplane().center(0,-(flange_width/2 - rib_thickness/2)).rect(flange_length-2*rib_thickness, rib_thickness).extrude(rib_height)
left_rib=plate.faces('>Z').workplane().center(-(flange_length/2 - rib_thickness/2),0).rect(rib_thickness, flange_width-2*rib_thickness).extrude(rib_height)
right_rib=plate.faces('>Z').workplane().center(flange_length/2 - rib_thickness/2,0).rect(rib_thickness, flange_width-2*rib_thickness).extrude(rib_height)
combined=plate.union(top_rib).union(bottom_rib).union(left_rib).union(right_rib)
result=combined