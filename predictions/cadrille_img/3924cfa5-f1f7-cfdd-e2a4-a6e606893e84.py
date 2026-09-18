import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-36))
w1=cq.Workplane('ZX',origin=(0,-62,0))
r=w0.sketch().arc((-10,-59),(10,-61),(29,-59)).close().assemble().reset().face(w0.sketch().segment((-10,59),(29,59)).arc((10,61),(-10,59)).assemble()).reset().face(w0.sketch().arc((31,-58),(61,0),(31,58)).segment((31,29)).arc((33,0),(31,-29)).close().assemble()).finalize().extrude(108).union(w1.sketch().segment((-64,-67),(-64,-66)).segment((64,-66)).segment((64,-67)).arc((0,100),(-64,-67)).assemble().finalize().extrude(162))