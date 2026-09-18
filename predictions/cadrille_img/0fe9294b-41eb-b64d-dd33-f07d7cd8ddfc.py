import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-50,0))
w1=cq.Workplane('ZX',origin=(0,-100,0))
r=w0.sketch().circle(79).push([(-29,46)]).circle(19,mode='s').push([(44,34)]).circle(13,mode='s').finalize().extrude(100).union(w1.sketch().arc((-93,-35),(-1,1),(78,-73)).segment((100,-73)).segment((100,13)).arc((96,15),(100,17)).segment((100,20)).segment((78,20)).arc((0,73),(-78,20)).segment((-81,20)).arc((-88,-8),(-93,-35)).assemble().finalize().extrude(199))