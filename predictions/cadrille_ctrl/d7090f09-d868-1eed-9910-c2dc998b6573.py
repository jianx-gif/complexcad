import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,28))
w1=cq.Workplane('XY',origin=(0,0,30))
r=w0.sketch().segment((-37,-7),(-25,-21)).segment((-24,-20)).arc((29,-22),(21,29)).segment((14,37)).segment((11,34)).arc((-20,25),(-29,-6)).arc((-33,-6),(-37,-7)).close().assemble().push([(0,-1)]).circle(32,mode='s').finalize().extrude(-28).union(w0.sketch().segment((-15,29),(15,29)).arc((0,41),(-15,29)).assemble().finalize().extrude(2)).union(w1.sketch().arc((19,-32),(37,0),(19,32)).segment((19,23)).arc((32,0),(19,-23)).close().assemble().finalize().extrude(-30))
