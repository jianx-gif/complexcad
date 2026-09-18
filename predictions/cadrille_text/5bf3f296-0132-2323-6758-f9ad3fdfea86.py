import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-62))
r=w0.sketch().face(w0.sketch().segment((92,-29),(92,29)).arc((39,0),(92,-29)).assemble()).finalize().extrude(200).union(w1.sketch().face(w1.sketch().arc((53,0),(55,0),(55,2)).arc((55,2),(53,4),(53,0)).assemble()).finalize().extrude(152))