import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,10))
r=w0.workplane(offset=-15/2).cylinder(15,25).union(w0.sketch().rect(80,60).circle(22,mode='s').finalize().extrude(-10)).union(w0.sketch().segment((-17,30),(-14,24)).segment((-12,25)).segment((-12,37)).arc((-15,33),(-17,30)).assemble().finalize().extrude(10))
