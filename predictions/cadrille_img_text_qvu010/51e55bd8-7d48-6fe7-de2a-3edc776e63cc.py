import cadquery as cq
w0=cq.Workplane('YZ',origin=(39,0,0))
w1=cq.Workplane('ZX',origin=(0,34,0))
r=w0.sketch().circle(100).circle(92,mode='s').finalize().extrude(39).union(w1.sketch().push([(0,-34)]).circle(36).push([(0,-34.5)]).rect(44,3,mode='s').finalize().extrude(-71))