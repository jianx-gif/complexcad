import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,30))
r=w0.sketch().arc((11,-44),(12,-43),(14,-43)).arc((12,-42),(11,-44)).assemble().finalize().extrude(-60).union(w0.sketch().segment((41,0),(41,1)).segment((45,1)).arc((-45,2),(45,0)).close().assemble().finalize().extrude(-30))