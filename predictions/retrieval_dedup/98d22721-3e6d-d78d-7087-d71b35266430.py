import cadquery as cq
panel_width=80.0
panel_height=60.0
panel_thickness=4.0
half_w=panel_width/2.0
half_h=panel_height/2.0
base=cq.Workplane('XY').moveTo(-half_w,-half_h).lineTo(half_w,-half_h).lineTo(half_w,half_h-5).lineTo(half_w+5,half_h-5).lineTo(half_w+5,half_h).lineTo(-half_w,half_h).close().extrude(panel_thickness)
rib_width=3.0
rib_depth=2.0
rib_inset=0.5
rib=cq.Workplane('XY').rect(rib_width,panel_height).extrude(rib_depth+rib_inset).translate((0,0,-rib_depth))
result=base.union(rib)
