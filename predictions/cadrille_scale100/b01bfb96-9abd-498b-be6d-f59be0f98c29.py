import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('XY',origin=(0,0,26))
r=w0.sketch().circle(39).circle(35,mode='s').finalize().extrude(-4).union(w0.sketch().circle(39).circle(35,mode='s').finalize().extrude(49)).union(w0.sketch().circle(23).circle(21,mode='s').finalize().extrude(49)).union(w1.sketch().segment((-34,-1),(-17,-1)).arc((0,-17),(17,-1)).segment((34,-1)).segment((34,1)).segment((17,1)).arc((0,17),(-17,1)).segment((-34,1)).close().assemble().finalize().extrude(5))