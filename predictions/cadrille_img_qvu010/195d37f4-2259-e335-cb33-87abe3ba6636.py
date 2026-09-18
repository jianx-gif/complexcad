import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,-89,0))
w1=cq.Workplane('XY',origin=(0,0,100))
r=w0.sketch().arc((-100,-55),(-77,-21),(-45,3)).arc((-45,13),(-36,17)).arc((-33,20),(-30,23)).segment((-30,40)).segment((-100,40)).close().assemble().finalize().extrude(10).union(w1.sketch().arc((-97,-66),(-20,93),(57,-66)).segment((57,-63)).arc((58,-59),(57,-55)).segment((57,-52)).segment((55,-52)).arc((-20,-88),(-95,-52)).segment((-97,-52)).segment((-97,-55)).arc((-98,-59),(-97,-63)).close().assemble().finalize().extrude(-200))