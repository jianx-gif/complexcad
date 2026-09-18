import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
r=w0.sketch().push([(0,0)]).circle(35).circle(33,mode='s').finalize().extrude(-30).union(w0.sketch().segment((-34,-10),(-28,-22)).segment((-24,-20)).arc((11,-33),(33,-3)).segment((37,-1)).segment((31,11)).segment((27,9)).arc((-7,22),(-29,-7)).close().assemble().push([(0,0)]).circle(33,mode='s').finalize().extrude(-30))
