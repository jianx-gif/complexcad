import cadquery as cq
w0=cq.Workplane('YZ',origin=(49,0,0))
w1=cq.Workplane('ZX',origin=(0,-33,0))
r=w0.sketch().circle(74).circle(67,mode='s').finalize().extrude(-65).union(w0.sketch().circle(100).circle(99,mode='s').finalize().extrude(29)).union(w1.sketch().arc((-36,-69),(35,0),(-36,69)).segment((-36,38)).arc((28,0),(-36,-38)).close().assemble().finalize().extrude(67))