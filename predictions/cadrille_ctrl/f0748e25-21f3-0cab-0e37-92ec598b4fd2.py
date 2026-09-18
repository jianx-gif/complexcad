import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
w1=cq.Workplane('ZX',origin=(0,6,0))
r=w0.sketch().segment((-40,-20),(39,-20)).segment((39,20)).segment((-40,20)).segment((-40,14)).arc((-39,13),(-40,12)).close().assemble().finalize().extrude(8).union(w0.sketch().segment((-21,1),(-19,-1)).segment((-19,-20)).segment((39,-20)).segment((39,20)).segment((-19,20)).segment((-19,3)).close().assemble().finalize().extrude(8)).union(w1.sketch().segment((-20,20),(20,20)).arc((0,40),(-20,20)).assemble().finalize().extrude(-6))
