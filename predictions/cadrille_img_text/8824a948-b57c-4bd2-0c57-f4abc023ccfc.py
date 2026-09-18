import cadquery as cq
w0=cq.Workplane('YZ',origin=(-48,0,0))
w1=cq.Workplane('ZX',origin=(0,-57,0))
r=w0.sketch().segment((-100,-60),(-91,-60)).arc((0,-96),(91,-60)).segment((100,-60)).segment((100,-42)).arc((96,0),(100,42)).segment((100,60)).segment((91,60)).arc((0,96),(-91,60)).segment((-100,60)).segment((-100,42)).arc((-96,0),(-100,-42)).close().assemble().circle(95,mode='s').finalize().extrude(128).union(w1.sketch().arc((-3,-48),(34,-43),(60,-17)).segment((87,-17)).segment((87,17)).segment((60,17)).arc((47,35),(28,46)).arc((27,4),(-3,-27)).close().assemble().finalize().extrude(135))