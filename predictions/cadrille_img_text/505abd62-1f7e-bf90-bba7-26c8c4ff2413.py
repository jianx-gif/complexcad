import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,87,0))
w1=cq.Workplane('ZX',origin=(0,30,0))
r=w0.sketch().arc((-97,-90),(0,-80),(97,-100)).segment((97,100)).segment((-97,100)).close().assemble().finalize().extrude(-135).union(w1.sketch().circle(97).circle(89,mode='s').finalize().extrude(-100))