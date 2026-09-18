import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,0,-10))
r=w0.sketch().segment((-97,56),(-96,56)).segment((-96,57)).close().assemble().reset().face(w0.sketch().segment((96,-77),(97,-56)).segment((96,-56)).close().assemble()).finalize().extrude(20).union(w0.sketch().circle(3).circle(2,mode='s').finalize().extrude(21))