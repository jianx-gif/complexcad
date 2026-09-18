import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
w1=cq.Workplane('ZX',origin=(0,-22,0))
r=w0.sketch().push([(0.5,0)]).rect(71,46).push([(1,0)]).circle(5,mode='s').finalize().extrude(-13).union(w0.sketch().push([(1,0)]).circle(10).push([(1.5,0)]).rect(17,10,mode='s').finalize().extrude(-10)).union(w1.sketch().push([(0,29.5)]).rect(6,45).push([(0,29)]).circle(2,mode='s').finalize().extrude(45))