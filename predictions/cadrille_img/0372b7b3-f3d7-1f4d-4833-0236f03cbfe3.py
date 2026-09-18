import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-96,0))
w1=cq.Workplane('ZX',origin=(0,-65,0))
r=w0.sketch().arc((-1,-1),(1,0),(2,-2)).arc((0,2),(-1,-1)).assemble().finalize().extrude(192).union(w1.sketch().arc((-70,-41),(100,0),(-70,41)).arc((-84,0),(-70,-41)).assemble().push([(8,11)]).circle(87,mode='s').finalize().extrude(123))