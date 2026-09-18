import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,100,0))
w1=cq.Workplane('ZX',origin=(0,74,0))
r=w0.sketch().arc((-46,39),(-79,-31),(-21,-84)).close().assemble().reset().face(w0.sketch().segment((-39,43),(46,-39)).arc((79,31),(21,84)).close().assemble()).finalize().extrude(-199).union(w1.sketch().circle(84).circle(60,mode='s').finalize().extrude(-53))