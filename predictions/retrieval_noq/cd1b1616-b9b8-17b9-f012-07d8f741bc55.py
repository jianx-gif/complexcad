import cadquery as cq

result = cq.Workplane('XY').box(10,10,5).faces('>Z').workplane().cskHole(5,2,8,1)
