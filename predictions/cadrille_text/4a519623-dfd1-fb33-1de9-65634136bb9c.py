import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-51))
w1=cq.Workplane('XY',origin=(0,0,-66))
r=w0.sketch().segment((-58,10),(-58,12)).segment((-56,12)).arc((-53,16),(-49,12)).segment((-47,12)).segment((-47,10)).segment((-49,10)).arc((-53,6),(-56,10)).close().assemble().finalize().extrude(-10).union(w1.sketch().segment((23,-11),(23,11)).arc((22,0),(23,-11)).assemble().finalize().extrude(133))