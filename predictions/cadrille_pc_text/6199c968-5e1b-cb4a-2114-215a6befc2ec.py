import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,80))
r=w0.sketch().circle(79).circle(67,mode='s').finalize().extrude(-160).union(w0.sketch().circle(100).push([(-34,-54)]).circle(4,mode='s').finalize().extrude(-20))