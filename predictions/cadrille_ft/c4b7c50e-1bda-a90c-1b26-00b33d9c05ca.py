import cadquery as cq
w0=cq.Workplane('YZ',origin=(76,0,0))
r=w0.sketch().segment((-76,-100),(76,-100)).segment((76,91)).segment((10,91)).segment((10,100)).segment((-10,100)).segment((-10,91)).segment((-76,91)).close().assemble().rect(144,192,mode='s').finalize().extrude(-152).union(w0.workplane(offset=-148/2).box(144,182,148))