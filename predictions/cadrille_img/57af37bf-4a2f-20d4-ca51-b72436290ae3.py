import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-85,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((-45,-95),(0,-79),(45,-95)).segment((45,-75)).arc((79,-26),(84,33)).segment((34,33)).arc((26,-37),(-45,-59)).close().assemble().finalize().extrude(170).union(w1.sketch().circle(100).circle(99,mode='s').finalize().extrude(-175))