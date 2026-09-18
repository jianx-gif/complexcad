import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,38,0))
w1=cq.Workplane('ZX',origin=(0,97,0))
r=w0.sketch().arc((-100,6),(-66,-76),(20,-80)).arc((69,-46),(93,9)).segment((100,9)).arc((0,89),(-100,6)).assemble().push([(0,-6)]).circle(89,mode='s').finalize().extrude(-78).union(w1.sketch().circle(82).circle(41,mode='s').finalize().extrude(-100))