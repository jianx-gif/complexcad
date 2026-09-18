import cadquery as cq
w0=cq.Workplane('YZ',origin=(33,0,0))
w1=cq.Workplane('YZ',origin=(43,0,0))
r=w0.sketch().circle(100).circle(92,mode='s').finalize().extrude(-76).union(w0.sketch().circle(82).reset().face(w0.sketch().segment((-40,-13),(38,-47)).segment((40,-43)).segment((-38,-9)).close().assemble(),mode='s').finalize().extrude(-18)).union(w1.sketch().circle(81).circle(47,mode='s').finalize().extrude(-28))