import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-2))
r=w0.sketch().segment((96,-49),(100,-49)).segment((100,-47)).close().assemble().finalize().extrude(45).union(w0.sketch().push([(100,0)]).circle(2).push([(99.5,0)]).rect(3,2,mode='s').finalize().extrude(50))