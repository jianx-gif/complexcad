import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-62,0))
w1=cq.Workplane('ZX',origin=(0,0,0))
r=w0.sketch().circle(100).circle(18,mode='s').finalize().extrude(89).union(w0.workplane(offset=124/2).cylinder(124,62)).union(w1.sketch().segment((-80,-30),(-70,-30)).arc((0,-73),(70,-30)).segment((80,-30)).segment((80,30)).segment((70,30)).arc((0,73),(-70,30)).segment((-80,30)).close().assemble().circle(20,mode='s').finalize().extrude(-10))