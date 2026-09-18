import cadquery as cq
w0=cq.Workplane('XY',origin=(0,0,-95))
w1=cq.Workplane('YZ',origin=(75,0,0))
r=w0.sketch().arc((-70,10),(11,38),(70,-25)).arc((15,94),(-70,10)).assemble().finalize().extrude(148).union(w1.sketch().arc((-58,-89),(-15,-91),(27,-78)).arc((30,-78),(32,-77)).arc((43,-72),(54,-67)).arc((-25,18),(28,99)).arc((-1,100),(-29,95)).arc((-34,95),(-39,94)).segment((-39,92)).arc((-45,88),(-51,84)).arc((-49,87),(-47,89)).arc((-99,-4),(-58,-89)).assemble().finalize().extrude(-134))