import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,1))
w1=cq.Workplane('XY',origin=(0,0,2))
r=w0.sketch().circle(21).circle(20,mode='s').finalize().extrude(4).union(w0.sketch().circle(30).circle(26,mode='s').finalize().extrude(79)).union(w1.sketch().arc((-19,-15),(-17,-15),(-17,-17)).arc((18,15),(-19,-15)).assemble().finalize().extrude(-2))
