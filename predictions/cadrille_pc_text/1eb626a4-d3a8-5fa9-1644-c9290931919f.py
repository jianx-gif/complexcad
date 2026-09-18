import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-88))
w1=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().push([(-8,0)]).circle(48).circle(41,mode='s').finalize().extrude(188).union(w1.sketch().circle(68).circle(14,mode='s').finalize().extrude(13))