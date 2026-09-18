import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,25))
r=w0.sketch().circle(35).circle(15,mode='s').push([(29,-1)]).circle(4,mode='s').finalize().extrude(-25).union(w0.sketch().circle(44).circle(36,mode='s').finalize().extrude(5))
