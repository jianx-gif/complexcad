import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((-53,15),(32,-58)).segment((53,-34)).segment((-32,39)).close().assemble().finalize().extrude(200)