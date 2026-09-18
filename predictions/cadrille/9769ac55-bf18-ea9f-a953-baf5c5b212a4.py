import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,19))
r=w0.sketch().circle(100).circle(88,mode='s').finalize().extrude(-38).union(w0.sketch().circle(90).push([(-11,-49)]).circle(22,mode='s').push([(0,0)]).rect(34,70,mode='s').finalize().extrude(-13))