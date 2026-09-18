import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,20))
r=w0.sketch().circle(35).push([(-31,-3)]).circle(2,mode='s').finalize().extrude(-20).union(w0.sketch().circle(35).circle(29,mode='s').finalize().extrude(-17)).union(w0.sketch().circle(45).circle(10,mode='s').finalize().extrude(4))