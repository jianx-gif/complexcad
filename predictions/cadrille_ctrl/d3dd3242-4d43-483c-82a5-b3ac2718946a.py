import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,30,0))
r=w0.sketch().rect(40,80).rect(36,76,mode='s').finalize().extrude(-60).union(w0.workplane(offset=-58/2).box(36,64,58))
