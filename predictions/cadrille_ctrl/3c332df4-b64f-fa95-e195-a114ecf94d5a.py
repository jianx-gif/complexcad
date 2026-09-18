import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,20,0))
w1=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().push([(0,40.5)]).rect(80,119).push([(0,40)]).circle(21,mode='s').finalize().extrude(2).union(w1.sketch().push([(40.5,0)]).rect(119,40).push([(1,17)]).circle(2,mode='s').push([(1.5,17)]).rect(3,4,mode='s').push([(1.5,16.5)]).rect(3,3).push([(60.5,0)]).rect(37,36,mode='s').finalize().extrude(80))
