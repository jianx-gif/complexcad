import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-10))
r=w0.sketch().segment((92,-43),(100,-43)).segment((100,-34)).segment((94,-34)).arc((93,-38),(92,-43)).assemble().finalize().extrude(-8).union(w0.sketch().push([(100,-50)]).circle(2).push([(99.5,-50)]).rect(3,2,mode='s').finalize().extrude(28)).union(w0.workplane(offset=28/2).moveTo(100,-50).cylinder(28,2))