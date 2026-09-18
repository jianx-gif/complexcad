import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-50,-50))
r=w0.sketch().segment((96,-41),(100,-19)).segment((96,-18)).close().assemble().finalize().extrude(100)