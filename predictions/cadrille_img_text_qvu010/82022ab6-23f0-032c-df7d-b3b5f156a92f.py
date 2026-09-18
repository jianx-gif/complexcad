import cadquery as cq
w0=cq.Workplane('YZ',origin=(79,0,0))
w1=cq.Workplane('YZ',origin=(100,0,0))
r=w0.sketch().arc((-45,-26),(-10,1),(31,-12)).arc((-8,46),(-45,-26)).assemble().finalize().extrude(-157).union(w1.sketch().segment((-92,-40),(-90,-40)).arc((0,-100),(90,-40)).segment((92,-40)).segment((92,-36)).arc((100,0),(92,36)).segment((92,40)).segment((90,40)).arc((0,100),(-90,40)).segment((-92,40)).segment((-92,36)).arc((-100,0),(-92,-36)).close().assemble().circle(46,mode='s').finalize().extrude(-14))