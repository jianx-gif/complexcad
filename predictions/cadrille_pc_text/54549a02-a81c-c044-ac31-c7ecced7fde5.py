import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-1))
r=w0.sketch().push([(11.5,-2.5)]).rect(177,103).push([(40,-2)]).rect(84,90,mode='s').finalize().extrude(-14).union(w0.sketch().push([(-19.5,-33.5)]).rect(161,41).push([(-64,-29)]).circle(7,mode='s').push([(67,1)]).circle(22).finalize().extrude(16))