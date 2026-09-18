import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((1,-5),(3,0),(1,5)).close().assemble().finalize().extrude(-200).union(w0.sketch().arc((-100,40),(-11,-1),(-10,-99)).arc((79,-58),(95,40)).arc((73,56),(59,79)).arc((-31,93),(-100,40)).assemble().finalize().extrude(-15))