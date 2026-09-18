import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
w1=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().circle(35).circle(25,mode='s').finalize().extrude(10).union(w0.sketch().circle(10).push([(0,6)]).circle(2,mode='s').finalize().extrude(3)).union(w1.sketch().rect(80,80).push([(3,-19)]).circle(4,mode='s').finalize().extrude(-5))
