import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-77,0))
w1=cq.Workplane('XY',origin=(0,0,60))
r=w0.sketch().push([(10,0)]).circle(90).circle(76,mode='s').finalize().extrude(100).union(w0.sketch().push([(9,0)]).circle(37).circle(22,mode='s').finalize().extrude(155)).union(w1.sketch().push([(0,-22)]).circle(39).circle(22,mode='s').finalize().extrude(-160))