import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-9))
r=w0.sketch().circle(67).rect(44,54,mode='s').finalize().extrude(6).union(w0.sketch().arc((-96,-22),(-82,-38),(-65,-50)).arc((94,33),(-78,-32)).close().assemble().circle(27,mode='s').finalize().extrude(18))