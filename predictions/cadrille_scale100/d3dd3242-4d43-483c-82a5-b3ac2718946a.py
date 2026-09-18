import cadquery as cq
w0=cq.Workplane('YZ',origin=(-40,0,0))
r=w0.sketch().rect(60,40).rect(56,36,mode='s').finalize().extrude(80).union(w0.sketch().rect(60,40).rect(36,36,mode='s').finalize().extrude(80))