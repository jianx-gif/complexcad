import cadquery as cq
result = cq.Workplane('XY').box(10,10,5).faces('>Z').workplane().rect(5,5).cutBlind(-5)
