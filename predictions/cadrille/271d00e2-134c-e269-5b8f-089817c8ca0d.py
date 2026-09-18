import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().circle(100).circle(98,mode='s').finalize().extrude(194).union(w0.sketch().circle(68).push([(-59,-26)]).circle(10,mode='s').finalize().extrude(200))