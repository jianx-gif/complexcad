import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,35))
r=w0.sketch().push([(0,21)]).circle(9).push([(0,20.5)]).rect(10,9,mode='s').finalize().extrude(-35).union(w0.sketch().push([(1,21)]).circle(9).push([(1,20.5)]).rect(10,7,mode='s').finalize().extrude(-35)).union(w0.sketch().push([(1,21)]).circle(9).push([(1,21.5)]).rect(10,11,mode='s').push([(1,21)]).circle(3).finalize().extrude(-35))
