import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,23))
w1=cq.Workplane('XY',origin=(0,0,25))
r=w0.sketch().segment((1,-30),(1,-28)).segment((3,-28)).segment((3,-29)).arc((-3,29),(1,-30)).assemble().finalize().extrude(-23).union(w0.sketch().segment((-30,1),(-17,-25)).segment((30,-1)).segment((17,25)).close().assemble().finalize().extrude(-23)).union(w1.sketch().arc((-10,-24),(0,-20),(10,-24)).segment((10,24)).segment((-10,24)).close().assemble().finalize().extrude(-20))