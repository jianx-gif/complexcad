import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-100))
r=w0.sketch().segment((-99,-15),(76,-15)).segment((76,-11)).segment((99,-11)).segment((99,11)).segment((76,11)).segment((76,15)).segment((53,15)).arc((2,69),(-50,15)).segment((-99,15)).close().assemble().finalize().extrude(200)