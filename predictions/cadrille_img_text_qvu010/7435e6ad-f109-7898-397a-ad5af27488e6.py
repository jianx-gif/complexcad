import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,14,0))
w1=cq.Workplane('ZX',origin=(0,87,0))
r=w0.sketch().segment((-97,-60),(97,-60)).segment((97,60)).segment((44,60)).arc((-21,3),(-97,34)).close().assemble().finalize().extrude(-41).union(w0.sketch().arc((-10,-1),(9,1),(-9,0)).segment((-7,0)).segment((-7,-1)).close().assemble().finalize().extrude(78)).union(w1.sketch().segment((-100,-65),(-91,-65)).arc((0,-96),(91,-65)).segment((100,-65)).segment((100,65)).segment((91,65)).arc((0,96),(-91,65)).segment((-100,65)).close().assemble().circle(33,mode='s').finalize().extrude(-143))