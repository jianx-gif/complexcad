import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-74,0))
w1=cq.Workplane('YZ',origin=(-100,0,0))
r=w0.sketch().segment((-36,-70),(16,-70)).segment((16,-55)).arc((-10,-16),(-14,29)).segment((-36,29)).close().assemble().finalize().extrude(-20).union(w0.sketch().segment((-71,-89),(-69,-90)).segment((-56,-55)).segment((-58,-54)).close().assemble().finalize().extrude(101)).union(w1.sketch().segment((-31,-99),(16,-99)).arc((31,-93),(46,-90)).arc((49,-82),(53,-75)).arc((10,-85),(-31,-74)).close().assemble().finalize().extrude(200))