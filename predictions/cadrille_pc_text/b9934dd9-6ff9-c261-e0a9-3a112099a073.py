import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-55))
r=w0.workplane(offset=-10/2).box(200,200,10).union(w0.sketch().circle(80).circle(64,mode='s').finalize().extrude(120))