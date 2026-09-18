import cadquery as cq
w0=cq.Workplane('XY',origin=(-57,0,-100))
r=w0.sketch().segment((-53,12),(-53,14)).arc((-54,13),(-53,12)).assemble().reset().face(w0.sketch().arc((26,-58),(27,-57),(28,-57)).segment((28,-55)).segment((29,-55)).arc((31,-53),(33,-55)).segment((34,-55)).segment((34,-57)).arc((35,-57),(36,-58)).close().assemble()).finalize().extrude(200)