import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-55))
w1=cq.Workplane('YZ',origin=(-25,0,0))
r=w0.sketch().rect(190,190).circle(35,mode='s').finalize().extrude(-13).union(w0.sketch().circle(100).circle(95,mode='s').finalize().extrude(99)).union(w1.sketch().push([(-3,0)]).circle(68).push([(-12,51)]).circle(14,mode='s').finalize().extrude(91))