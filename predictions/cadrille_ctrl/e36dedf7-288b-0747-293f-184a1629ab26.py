import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,5))
r=w0.sketch().circle(2).rect(2,2,mode='s').finalize().extrude(-37).union(w0.sketch().circle(48).circle(3,mode='s').finalize().extrude(2)).union(w0.sketch().circle(40).push([(11,5)]).circle(23,mode='s').finalize().extrude(25))
