import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,90,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().arc((-60,-46),(1,-1),(60,-46)).segment((60,46)).segment((-60,46)).close().assemble().finalize().extrude(-180).union(w1.sketch().circle(90).circle(89,mode='s').finalize().extrude(-47))