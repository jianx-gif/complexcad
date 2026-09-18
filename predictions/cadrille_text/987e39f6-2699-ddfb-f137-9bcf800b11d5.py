import cadquery as cq
w0=cq.Workplane('XY',origin=(-50,-50,-100))
w1=cq.Workplane('XY',origin=(-50,-50,-100))
r=w0.sketch().circle(50).circle(34,mode='s').finalize().extrude(200).union(w1.sketch().face(w1.sketch().segment((0,0),(100,0)).segment((100,0),(100,100)).segment((100,100),(0,100)).segment((0,100),(0,0)).assemble()).finalize().extrude(100))