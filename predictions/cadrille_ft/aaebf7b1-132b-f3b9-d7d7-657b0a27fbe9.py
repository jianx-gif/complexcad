import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-55))
w1=cq.Workplane('ZX',origin=(0,56,0))
r=w0.workplane(offset=-13/2).box(190,190,13).union(w0.sketch().circle(100).circle(95,mode='s').finalize().extrude(89)).union(w1.sketch().push([(0,-1)]).circle(90).push([(50,-10)]).circle(15,mode='s').finalize().extrude(-137))