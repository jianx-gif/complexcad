import cadquery as cq
w0=cq.Workplane('YZ',origin=(-77,0,0))
w1=cq.Workplane('ZX',origin=(0,33,0))
r=w0.sketch().segment((16,100),(29,86)).segment((29,86),(32,86)).segment((32,86),(45,74)).segment((45,74),(58,60)).arc((42,83),(16,100)).assemble().finalize().extrude(40).union(w0.sketch().push([(0,-71)]).circle(29).circle(23,mode='s').finalize().extrude(163)).union(w1.sketch().push([(0,-64)]).circle(23).circle(14,mode='s').finalize().extrude(-65))