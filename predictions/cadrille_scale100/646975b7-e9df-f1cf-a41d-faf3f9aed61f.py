import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,35))
w1=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().push([(1,25)]).circle(5).push([(1,25.5)]).rect(2,5,mode='s').finalize().extrude(-35).union(w0.sketch().push([(1,25)]).circle(5).push([(1,25.5)]).rect(2,3,mode='s').finalize().extrude(-35)).union(w1.sketch().push([(1,25)]).circle(5).push([(1,25.5)]).rect(2,3,mode='s').finalize().extrude(-10))