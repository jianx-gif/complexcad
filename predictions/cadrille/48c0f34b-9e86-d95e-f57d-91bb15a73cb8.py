import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,19))
w1=cq.Workplane('ZX',origin=(0,-21,0))
r=w0.sketch().push([(0,-1)]).circle(81).circle(47,mode='s').finalize().extrude(-48).union(w0.sketch().circle(100).circle(98,mode='s').finalize().extrude(-32)).union(w1.sketch().circle(42).circle(26,mode='s').finalize().extrude(78))