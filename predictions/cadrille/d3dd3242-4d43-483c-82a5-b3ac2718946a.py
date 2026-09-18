import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().segment((-75,-50),(75,-50)).segment((75,50)).segment((73,50)).segment((73,48)).segment((70,48)).segment((70,50)).segment((-75,50)).close().assemble().rect(140,90,mode='s').finalize().extrude(-200)