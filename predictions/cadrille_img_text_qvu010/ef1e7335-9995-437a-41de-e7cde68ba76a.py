import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,96,0))
w1=cq.Workplane('ZX',origin=(0,100,0))
r=w0.sketch().segment((-70,-46),(70,-46)).segment((70,46)).segment((-70,46)).segment((-70,45)).segment((-32,45)).segment((-32,-45)).segment((-70,-45)).close().assemble().finalize().extrude(-133).union(w1.sketch().arc((-100,-45),(-74,-67),(-43,-85)).segment((-43,85)).arc((-74,67),(-100,45)).close().assemble().finalize().extrude(-200))