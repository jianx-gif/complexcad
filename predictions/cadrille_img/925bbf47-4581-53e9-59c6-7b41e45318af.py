import cadquery as cq
w0=cq.Workplane('YZ',origin=(-100,0,0))
w1=cq.Workplane('ZX',origin=(0,-18,0))
r=w0.sketch().segment((19,39),(39,52)).arc((28,48),(19,39)).assemble().finalize().extrude(198).union(w1.sketch().arc((-59,83),(-49,57),(-38,32)).arc((74,21),(-27,-22)).arc((-33,-35),(-40,-47)).segment((92,-47)).segment((92,83)).close().assemble().push([(22,23)]).circle(53,mode='s').push([(22,22.5)]).rect(84,75).finalize().extrude(18))