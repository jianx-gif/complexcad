import cadquery as cq
base = cq.Workplane('XY').rect(80,30).extrude(6)
flange1 = cq.Workplane('XY').box(80,12,8).translate((0,15-6-0.5,6+8/2))
result = base.union(flange1)
