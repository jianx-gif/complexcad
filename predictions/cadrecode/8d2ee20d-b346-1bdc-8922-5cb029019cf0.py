import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-20))
r=w0.sketch().circle(100).circle(87,mode='s').circle(83).finalize().extrude(30).union(w0.sketch().circle(37).push([(-23,-10)]).circle(10,mode='s').finalize().extrude(40))