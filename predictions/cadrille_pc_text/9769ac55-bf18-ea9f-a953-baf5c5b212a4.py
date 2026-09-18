import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,19))
r=w0.sketch().circle(100).circle(88,mode='s').finalize().extrude(-38).union(w0.sketch().rect(160,148).push([(-13,-40)]).circle(22,mode='s').push([(10,47)]).circle(17,mode='s').finalize().extrude(-13))