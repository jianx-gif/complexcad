import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-58,0))
w1=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().circle(100).circle(93,mode='s').finalize().extrude(150).union(w1.sketch().push([(57,-58)]).circle(34).push([(57.5,-58)]).rect(39,24,mode='s').finalize().extrude(-20))