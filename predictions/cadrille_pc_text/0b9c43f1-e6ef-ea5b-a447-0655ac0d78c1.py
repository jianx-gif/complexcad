import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,95,0))
r=w0.sketch().circle(51).circle(2,mode='s').finalize().extrude(-195).union(w0.sketch().circle(63).circle(59,mode='s').finalize().extrude(-153)).union(w0.sketch().arc((-31,70),(-77,-29),(21,-82)).segment((21,-86)).segment((31,-86)).segment((31,-79)).arc((80,29),(-28,74)).segment((-28,70)).close().assemble().finalize().extrude(5))