import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-31,0))
w1=cq.Workplane('ZX',origin=(0,-89,0))
r=w0.sketch().circle(100).circle(69,mode='s').finalize().extrude(6).union(w1.sketch().arc((-62,59),(-60,57),(-59,54)).arc((58,-57),(-38,63)).arc((-40,66),(-42,69)).arc((55,-84),(-62,59)).assemble().finalize().extrude(178))