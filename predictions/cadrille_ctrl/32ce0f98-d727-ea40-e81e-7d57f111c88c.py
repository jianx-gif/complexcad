import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,2))
w1=cq.Workplane('XY',origin=(0,0,1))
r=w0.sketch().circle(10).circle(8,mode='s').finalize().extrude(-2).union(w0.sketch().circle(10).circle(9,mode='s').finalize().extrude(98)).union(w1.sketch().arc((13,-1),(15,0),(16,3)).arc((-15,1),(15,3)).arc((14,1),(13,-1)).assemble().finalize().extrude(99))
