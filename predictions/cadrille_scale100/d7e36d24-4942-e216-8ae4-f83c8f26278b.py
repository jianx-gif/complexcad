import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,50))
w1=cq.Workplane('XY',origin=(0,0,45))
r=w0.sketch().circle(40).circle(25,mode='s').finalize().extrude(-45).union(w0.sketch().segment((-15,-3),(-3,-15)).segment((15,3)).segment((3,15)).close().assemble().finalize().extrude(15)).union(w1.sketch().circle(15).rect(18,12,mode='s').finalize().extrude(19))