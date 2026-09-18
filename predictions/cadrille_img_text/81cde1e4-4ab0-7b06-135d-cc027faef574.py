import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,10,0))
w1=cq.Workplane('YZ',origin=(88,0,0))
r=w0.sketch().push([(0,14)]).circle(69).circle(18,mode='s').finalize().extrude(-62).union(w0.sketch().segment((-55,-59),(55,-59)).segment((55,59)).segment((53,59)).segment((55,58)).segment((55,59)).segment((-55,59)).close().assemble().finalize().extrude(32)).union(w1.sketch().segment((-87,-55),(-87,55)).arc((-92,0),(-87,-55)).assemble().finalize().extrude(-146))