import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-11,0))
w1=cq.Workplane('XY',origin=(0,0,-8))
r=w0.sketch().arc((-13,100),(-3,1),(13,-96)).segment((13,-87)).arc((-2,-64),(2,-38)).segment((1,-38)).segment((1,-34)).segment((2,-34)).arc((2,21),(-13,100)).assemble().finalize().extrude(22).union(w1.sketch().push([(-84,0)]).circle(13).circle(3,mode='s').finalize().extrude(21))