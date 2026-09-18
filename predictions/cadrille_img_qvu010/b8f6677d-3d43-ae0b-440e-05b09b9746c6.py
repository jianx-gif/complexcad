import cadquery as cq
w0=cq.Workplane('YZ',origin=(100,0,0))
w1=cq.Workplane('ZX',origin=(0,-45,0))
r=w0.sketch().arc((-45,-63),(-44,-63),(-43,-64)).segment((45,63)).segment((43,64)).close().assemble().push([(59,0)]).circle(39).circle(33,mode='s').finalize().extrude(-200).union(w0.sketch().segment((-45,-98),(45,-98)).segment((45,-68)).arc((89,0),(45,68)).segment((45,98)).segment((-45,98)).segment((-45,68)).arc((-89,0),(-45,-68)).close().assemble().finalize().extrude(-169)).union(w1.sketch().push([(0,39)]).circle(35).circle(32,mode='s').finalize().extrude(10))