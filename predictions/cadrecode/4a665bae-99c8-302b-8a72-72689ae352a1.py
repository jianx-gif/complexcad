import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
w1=cq.Workplane('ZX',origin=(0,16,0))
r=w0.sketch().push([(-6,0)]).rect(76,50).rect(56,30,mode='s').finalize().extrude(-200).union(w1.sketch().segment((-10,22),(10,22)).segment((10,44)).arc((0,41),(-10,42)).close().assemble().finalize().extrude(-40))