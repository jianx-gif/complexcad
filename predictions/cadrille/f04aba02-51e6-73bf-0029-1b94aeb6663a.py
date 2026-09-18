import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,1))
r=w0.sketch().rect(200,150).push([(-43,-56)]).rect(94,12,mode='s').finalize().extrude(-10).union(w0.workplane(offset=8/2).box(50,100,8))