import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,41,0))
r=w0.sketch().segment((-76,-67),(-60,-77)).segment((76,60)).segment((60,77)).close().assemble().finalize().extrude(-158).union(w1.sketch().circle(15).circle(3,mode='s').finalize().extrude(-141))