import cadquery as cq
w0=cq.Workplane('XY',origin=(-80,-100,-8))
w1=cq.Workplane('XY',origin=(-40,-100,-8))
r=w0.sketch().face(w0.sketch().segment((0,0),(160,0)).segment((160,0),(160,200)).segment((160,200),(0,200)).segment((0,200),(0,0)).assemble()).finalize().extrude(27).union(w1.sketch().face(w1.sketch().segment((0,0),(80,0)).segment((80,0),(80,200)).segment((80,200),(0,200)).segment((0,200),(0,0)).assemble()).finalize().extrude(27))