import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,76))
r=w0.sketch().segment((66,-54),(66,-52)).segment((68,-52)).arc((-61,60),(66,-54)).assemble().circle(72,mode='s').finalize().extrude(-152).union(w0.sketch().circle(100).circle(73,mode='s').finalize().extrude(-23))