import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,4))
r=w0.sketch().rect(200,134).push([(-78,19)]).circle(3,mode='s').push([(0,0)]).circle(36,mode='s').push([(0,58)]).rect(4,2,mode='s').finalize().extrude(-8)