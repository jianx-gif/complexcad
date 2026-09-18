import cadquery as cq
w0=cq.Workplane('XY',origin=(-35,-35,-100))
r=w0.sketch().segment((-35,29),(35,29)).arc((0,45),(-35,29)).assemble().finalize().extrude(190).union(w0.sketch().segment((-7,-90),(7,-90)).segment((7,-90),(7,90)).segment((7,90),(-7,90)).close().assemble().finalize().extrude(200))