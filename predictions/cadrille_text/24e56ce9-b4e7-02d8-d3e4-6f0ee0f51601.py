import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
w1=cq.Workplane('XY',origin=(0,0,-60))
r=w0.sketch().circle(30).circle(27,mode='s').finalize().extrude(200).union(w1.sketch().arc((-3,-91),(1,-91),(3,-90)).segment((-3,-90)).close().assemble().finalize().extrude(-39))