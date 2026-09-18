import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-60))
r=w0.sketch().circle(100).circle(44,mode='s').finalize().extrude(100).union(w0.sketch().circle(87).push([(-37,37.5)]).rect(10,13,mode='s').finalize().extrude(120))