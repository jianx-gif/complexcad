import cadquery as cq
w0=cq.Workplane('YZ',origin=(98,0,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.workplane(offset=-195/2).moveTo(-6.5,0).box(83,46,195).union(w1.sketch().segment((-50,-25),(50,-25)).segment((50,-10)).arc((46,1),(50,12)).segment((50,25)).segment((-50,25)).close().assemble().rect(96,46,mode='s').finalize().extrude(-200))