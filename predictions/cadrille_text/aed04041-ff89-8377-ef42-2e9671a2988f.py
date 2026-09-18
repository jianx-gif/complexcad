import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-1))
w1=cq.Workplane('XY',origin=(-100,0,-33))
r=w0.sketch().segment((-99,99),(-98,99)).segment((-98,100)).close().assemble().finalize().extrude(-65).union(w1.sketch().segment((25,-11),(25,-9)).arc((24,-7),(25,-5)).segment((25,-3)).arc((23,-7),(25,-11)).assemble().finalize().extrude(100))