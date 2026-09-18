import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,16,0))
w1=cq.Workplane('ZX',origin=(0,96,0))
r=w0.sketch().segment((-100,-84),(100,-84)).segment((100,84)).segment((-100,84)).segment((-100,-13)).segment((-98,-13)).segment((-98,-16)).segment((-100,-16)).close().assemble().reset().face(w0.sketch().segment((-60,-16),(-47,-33)).segment((-13,-8)).arc((15,-16),(13,14)).segment((60,50)).segment((47,67)).close().assemble(),mode='s').finalize().extrude(-30).union(w1.sketch().arc((-1,-1),(0,1),(1,-1)).segment((1,1)).segment((-1,1)).close().assemble().finalize().extrude(-193))