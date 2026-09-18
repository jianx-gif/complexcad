import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,0))
r=w0.sketch().segment((12,38),(12,39)).arc((11,37),(14,38)).close().assemble().finalize().extrude(-60).union(w0.sketch().segment((22,26),(22,33)).arc((-26,-31),(25,31)).segment((25,26)).close().assemble().push([(0,-1)]).circle(15,mode='s').finalize().extrude(60))