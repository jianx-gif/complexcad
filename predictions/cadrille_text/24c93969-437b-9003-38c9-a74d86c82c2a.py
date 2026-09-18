import cadquery as cq
w0=cq.Workplane('XY',origin=(-100,-100,-100))
r=w0.sketch().segment((92,-100),(100,-100)).segment((100,-98)).close().assemble().finalize().extrude(200)