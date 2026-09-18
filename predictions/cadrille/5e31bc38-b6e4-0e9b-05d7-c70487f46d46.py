import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-2,0))
w1=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().arc((-97,18),(-96,-30),(-69,-70)).segment((-69,-82)).segment((-10,-82)).arc((100,7),(-18,96)).arc((-69,68),(-97,18)).assemble().push([(1,0)]).circle(60,mode='s').finalize().extrude(4).union(w0.sketch().push([(1,0)]).circle(88).circle(69,mode='s').finalize().extrude(20)).union(w1.workplane(offset=38/2).moveTo(-83,-2).cylinder(38,16))