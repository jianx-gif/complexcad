import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-35,0))
w1=cq.Workplane('ZX',origin=(0,-37,0))
r=w0.sketch().segment((-28,-33),(28,-33)).segment((28,33)).segment((-28,33)).segment((-28,17)).arc((-25,15),(-28,13)).close().assemble().finalize().extrude(-55).union(w0.sketch().circle(100).circle(57,mode='s').finalize().extrude(28)).union(w1.sketch().arc((-95,29),(92,-40),(-92,40)).arc((-92,34),(-95,29)).assemble().finalize().extrude(107))