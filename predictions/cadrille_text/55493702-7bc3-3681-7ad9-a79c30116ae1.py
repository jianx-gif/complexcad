import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((90,-83),(100,-83)).segment((100,-77)).arc((95,-80),(90,-83)).assemble().finalize().extrude(100).union(w0.sketch().push([(50,0)]).circle(50).circle(47,mode='s').finalize().extrude(100))