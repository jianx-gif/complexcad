import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,78,0))
r=w0.sketch().arc((-22,4),(19,-12),(-17,15)).arc((-16,7),(-22,4)).assemble().push([(1,0)]).circle(2,mode='s').finalize().extrude(-78).union(w0.sketch().segment((-34,6),(-31,1)).arc((-28,-17),(-14,-29)).segment((-11,-34)).segment((-7,-31)).arc((17,-29),(31,-9)).segment((34,-6)).segment((31,-1)).arc((28,17),(14,29)).segment((11,34)).segment((7,31)).arc((-17,29),(-31,9)).close().assemble().finalize().extrude(2))
