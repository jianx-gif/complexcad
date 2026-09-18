import cadquery as cq
w0=cq.Workplane('ZX',origin=(0,96,0))
w1=cq.Workplane('YZ',origin=(42,0,0))
r=w0.sketch().arc((-68,-59),(-5,-46),(60,-59)).arc((73,-27),(99,-3)).arc((-31,84),(-68,-59)).assemble().finalize().extrude(-163).union(w1.sketch().push([(-13,0)]).circle(87).circle(63,mode='s').finalize().extrude(-132))