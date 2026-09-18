import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,7))
r=w0.sketch().rect(200,100).push([(-65,-33)]).circle(5,mode='s').push([(0,0)]).rect(16,98,mode='s').push([(65,-33)]).circle(5,mode='s').finalize().extrude(-20).union(w0.workplane(offset=7/2).cylinder(7,30))