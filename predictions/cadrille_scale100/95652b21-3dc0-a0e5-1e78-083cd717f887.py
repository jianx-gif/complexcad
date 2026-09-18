import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,8))
r=w0.sketch().circle(27).push([(-14,-1)]).circle(3,mode='s').finalize().extrude(-16).union(w0.sketch().circle(50).circle(12,mode='s').finalize().extrude(-8))