import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-1,-1))
r=w0.sketch().segment((95,-89),(100,-89)).segment((100,-86)).close().assemble().finalize().extrude(24).union(w0.sketch().push([(0,1)]).circle(8).push([(0,0)]).circle(3,mode='s').finalize().extrude(100))