import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,20,0))
w1=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().push([(0,40.5)]).rect(80,119).push([(0,40)]).circle(20,mode='s').finalize().extrude(2).union(w1.sketch().push([(40,0)]).rect(120,40).rect(40,36,mode='s').push([(60.5,0)]).rect(37,36,mode='s').finalize().extrude(80))