import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().segment((99,-10),(99,-8)).segment((100,-8)).arc((96,-10),(100,-10)).close().assemble().finalize().extrude(-200)