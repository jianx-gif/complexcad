import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,15))
w1=cq.Workplane('XY',origin=(0,0,-1))
r=w0.sketch().push([(-19.5,-2.5)]).rect(161,103).push([(-19.5,-2.5,-2.5)]).rect(123,23,mode='s').push([(-65,-32)]).circle(7,mode='s').finalize().extrude(-23).union(w1.sketch().push([(11.5,-2.5)]).rect(177,103).push([(12,-2.5)]).rect(102,71,mode='s').push([(77,14)]).circle(12,mode='s').finalize().extrude(-14))