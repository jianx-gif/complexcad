import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-11))
r=w0.sketch().segment((-100,-39),(100,-39)).segment((100,-13)).segment((99,-13)).segment((99,-10)).segment((100,-10)).segment((100,28)).segment((-100,28)).close().assemble().push([(30,-36)]).circle(3,mode='s').finalize().extrude(11).union(w0.sketch().arc((-1,28),(0,33),(1,39)).segment((-1,39)).close().assemble().finalize().extrude(22))