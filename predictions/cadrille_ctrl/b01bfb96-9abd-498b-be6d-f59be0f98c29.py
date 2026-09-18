import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().circle(39).circle(35,mode='s').finalize().extrude(-4).union(w0.sketch().circle(39).circle(35,mode='s').finalize().extrude(49)).union(w0.sketch().circle(23).circle(21,mode='s').finalize().extrude(49)).union(w1.sketch().circle(21).push([(1,19)]).circle(2,mode='s').finalize().extrude(30))
