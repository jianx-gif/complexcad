import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-20))
r=w0.sketch().circle(100).circle(98,mode='s').finalize().extrude(30).union(w0.sketch().segment((-48,-10),(-48,10)).arc((-50,0),(-48,-10)).assemble().reset().face(w0.sketch().arc((-47,-11),(0,-47),(47,-11)).close().assemble()).reset().face(w0.sketch().segment((-47,11),(47,11)).arc((0,47),(-47,11)).assemble()).finalize().extrude(40))