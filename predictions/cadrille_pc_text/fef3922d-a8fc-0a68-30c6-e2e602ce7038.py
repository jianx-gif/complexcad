import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-95))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().circle(45).circle(34,mode='s').finalize().extrude(121).union(w0.sketch().circle(32).push([(21,10)]).circle(8,mode='s').finalize().extrude(195)).union(w1.sketch().circle(15).circle(10,mode='s').finalize().extrude(155))