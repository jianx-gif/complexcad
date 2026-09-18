import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,25))
r=w0.sketch().circle(55).circle(27,mode='s').finalize().extrude(-100).union(w0.sketch().circle(74).circle(68,mode='s').finalize().extrude(-47)).union(w0.sketch().circle(100).push([(-12,88)]).circle(10,mode='s').finalize().extrude(50))